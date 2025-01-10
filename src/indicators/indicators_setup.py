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



import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator
from ta.volatility import BollingerBands

def calculate_indicators(df):
    """Calculate and add indicators to the DataFrame."""
    df['RSI'] = RSIIndicator(df['Close']).rsi()
    macd = MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    bb = BollingerBands(df['Close'])
    df['BB_Upper'] = bb.bollinger_hband()
    df['BB_Lower'] = bb.bollinger_lband()
    df['SMA'] = SMAIndicator(df['Close'], window=50).sma_indicator()

    # Adjust RTD_Trend logic
    df['RTD_Trend'] = df['SMA'] > df['Close']
    df['RTD_Trend'] = df['RTD_Trend'].apply(lambda x: 'UP' if x else 'DOWN')

    df.fillna(method='bfill', inplace=True)
    df.fillna(method='ffill', inplace=True)
    return df
