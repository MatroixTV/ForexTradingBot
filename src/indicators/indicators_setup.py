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
from ta.trend import MACD
from src.indicators.xmode import XMode
from src.indicators.rtd import RTD
from src.indicators.maw import MAW


def calculate_indicators(df):
    """
    Calculate technical indicators and append them to the DataFrame.
    :param df: DataFrame with OHLCV data.
    :return: DataFrame with calculated indicators.
    """
    # Calculate RSI
    rsi_indicator = RSIIndicator(close=df['Close'], window=14)
    df['RSI'] = rsi_indicator.rsi()

    # Calculate MACD and Signal Line
    macd = MACD(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()

    # Calculate Bollinger Bands
    df['BB_Upper'] = df['Close'].rolling(window=20).mean() + 2 * df['Close'].rolling(window=20).std()
    df['BB_Lower'] = df['Close'].rolling(window=20).mean() - 2 * df['Close'].rolling(window=20).std()

    # Calculate ATR
    df['ATR'] = df['High'] - df['Low']

    # Calculate XMode Levels
    xmode = XMode(df)
    xmode_levels = xmode.calculate_levels()
    df = pd.concat([df, xmode_levels], axis=1)

    # Calculate RTD
    rtd = RTD(df)
    rtd_values = rtd.calculate_rtd()
    df = pd.concat([df, rtd_values], axis=1)

    # Calculate MAW
    maw = MAW(df)
    maw_values = maw.calculate_maw()
    df = pd.concat([df, maw_values], axis=1)

    # Fill NaN values
    df.fillna(method="bfill", inplace=True)
    df.fillna(method="ffill", inplace=True)

    print(f"Indicators calculated: {list(df.columns)}")
    return df
