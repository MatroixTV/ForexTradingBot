# import pandas as pd
# import numpy as np
#
# def calculate_rsi(series, period=14):
#     delta = series.diff()
#     gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
#     loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
#     rs = gain / loss
#     return 100 - (100 / (1 + rs))
#
# def calculate_macd(series, fast=12, slow=26, signal=9):
#     fast_ema = series.ewm(span=fast, min_periods=1).mean()
#     slow_ema = series.ewm(span=slow, min_periods=1).mean()
#     macd = fast_ema - slow_ema
#     signal_line = macd.ewm(span=signal, min_periods=1).mean()
#     return macd, signal_line
#
# def calculate_bollinger_bands(series, window=20):
#     sma = series.rolling(window=window).mean()
#     std = series.rolling(window=window).std()
#     upper_band = sma + (2 * std)
#     lower_band = sma - (2 * std)
#     return upper_band, lower_band
#
# def calculate_xmode(series):
#     rolling_mean = series.rolling(window=14).mean()
#     rolling_std = series.rolling(window=14).std()
#     return (series - rolling_mean) / rolling_std
#
# def calculate_adx(df, period=14):
#     high = df["High"]
#     low = df["Low"]
#     close = df["Close"]
#
#     tr1 = high - low
#     tr2 = abs(high - close.shift(1))
#     tr3 = abs(low - close.shift(1))
#     tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
#
#     plus_dm = high.diff()
#     minus_dm = low.diff()
#
#     plus_dm[plus_dm < 0] = 0
#     minus_dm[minus_dm > 0] = 0
#
#     tr_smooth = tr.rolling(window=period).sum()
#     plus_dm_smooth = plus_dm.rolling(window=period).sum()
#     minus_dm_smooth = minus_dm.rolling(window=period).sum()
#
#     plus_di = 100 * (plus_dm_smooth / tr_smooth)
#     minus_di = 100 * (minus_dm_smooth / tr_smooth)
#     dx = 100 * (abs(plus_di - minus_di) / (plus_di + minus_di))
#
#     adx = dx.rolling(window=period).mean()
#     return adx
#
# def add_indicators(df):
#     if not all(col in df.columns for col in ["Close", "High", "Low"]):
#         raise KeyError("The dataframe must contain 'Close', 'High', and 'Low' columns.")
#
#     df["RSI"] = calculate_rsi(df["Close"], 14)
#     df["MACD"], df["MACD_Signal"] = calculate_macd(df["Close"])
#     df["BB_Upper"], df["BB_Lower"] = calculate_bollinger_bands(df["Close"])
#     df["XMODE"] = calculate_xmode(df["Close"])
#     df["ADX"] = calculate_adx(df)
#
#     # Forward-fill and back-fill for any remaining NaN values
#     df.fillna(method="ffill", inplace=True)
#     df.fillna(method="bfill", inplace=True)
#
#     return df


import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD, AverageTrueRange


def calculate_indicators(df):
    """
    Calculate all indicators and add them to the DataFrame.
    """
    # Ensure required columns are present
    required_columns = ['Close', 'High', 'Low', 'Open']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Bollinger Bands
    bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['BB_Upper'] = bb.bollinger_hband()
    df['BB_Lower'] = bb.bollinger_lband()

    # RSI
    rsi = RSIIndicator(close=df['Close'], window=14)
    df['RSI'] = rsi.rsi()

    # MACD
    macd = MACD(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()

    # ATR
    atr = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'], window=14)
    df['ATR'] = atr.average_true_range()

    # MAMA/FAMA
    df['MAMA'], df['FAMA'] = calculate_mama_fama(df['Close'])

    # RTD
    df['RTD_Trend'] = calculate_rtd(df)

    # Fill NaN values
    df.fillna(method='bfill', inplace=True)
    df.fillna(method='ffill', inplace=True)

    print(f"Indicators calculated: {list(df.columns)}")
    return df


def calculate_mama_fama(series, fast_limit=0.5, slow_limit=0.05):
    """
    Calculate MAMA (MESA Adaptive Moving Average) and FAMA (Following Adaptive Moving Average).
    """
    mama = np.zeros(len(series))
    fama = np.zeros(len(series))
    smooth = np.zeros(len(series))
    detrender = np.zeros(len(series))
    period = np.zeros(len(series))
    phase = np.zeros(len(series))
    alpha = np.zeros(len(series))

    for i in range(1, len(series)):
        smooth[i] = (4 * series[i] + 3 * series[i - 1] + 2 * series[i - 2] + series[i - 3]) / 10
        detrender[i] = smooth[i] - smooth[i - 1]
        phase[i] = np.arctan2(detrender[i], detrender[i - 1]) if detrender[i - 1] != 0 else 0
        period[i] = 0.9 * period[i - 1] + 0.1 * (6.28 / phase[i]) if phase[i] != 0 else period[i - 1]
        alpha[i] = 2 / (period[i] + 1)
        mama[i] = alpha[i] * series[i] + (1 - alpha[i]) * mama[i - 1]
        fama[i] = 0.5 * alpha[i] * mama[i] + (1 - 0.5 * alpha[i]) * fama[i - 1]

    return pd.Series(mama), pd.Series(fama)


def calculate_rtd(df, period=14):
    """
    Calculate Relative Trend Direction (RTD).
    """
    df['Price_Change'] = df['Close'].diff()
    rtd = df['Price_Change'].rolling(window=period).sum()
    return rtd
