import pandas as pd
import numpy as np

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(series, fast=12, slow=26, signal=9):
    fast_ema = series.ewm(span=fast, min_periods=1).mean()
    slow_ema = series.ewm(span=slow, min_periods=1).mean()
    macd = fast_ema - slow_ema
    signal_line = macd.ewm(span=signal, min_periods=1).mean()
    return macd, signal_line

def calculate_bollinger_bands(series, window=20):
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper_band = sma + (2 * std)
    lower_band = sma - (2 * std)
    return upper_band, lower_band

def calculate_xmode(series):
    rolling_mean = series.rolling(window=14).mean()
    rolling_std = series.rolling(window=14).std()
    return (series - rolling_mean) / rolling_std

def calculate_atr(df, period=14):
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

def calculate_adx(df, period=14):
    high_diff = df['High'].diff()
    low_diff = df['Low'].diff()
    plus_dm = np.where((high_diff > low_diff) & (high_diff > 0), high_diff, 0)
    minus_dm = np.where((low_diff > high_diff) & (low_diff > 0), low_diff, 0)
    tr = calculate_atr(df, 1)  # True range for single period
    plus_di = (plus_dm.rolling(window=period).sum() / tr.rolling(window=period).sum()) * 100
    minus_di = (minus_dm.rolling(window=period).sum() / tr.rolling(window=period).sum()) * 100
    dx = (np.abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.rolling(window=period).mean()
    return adx

def add_indicators(df):
    required_columns = {"High", "Low", "Close", "Volume"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise KeyError(f"The dataframe is missing required columns: {missing_columns}")

    df["RSI"] = calculate_rsi(df["Close"], 14)
    df["MACD"], df["MACD_Signal"] = calculate_macd(df["Close"])
    df["BB_Upper"], df["BB_Lower"] = calculate_bollinger_bands(df["Close"])
    df["XMODE"] = calculate_xmode(df["Close"])
    df["ATR"] = calculate_atr(df)
    df["ADX"] = calculate_adx(df)

    # Forward-fill and back-fill for any remaining NaN values
    df.fillna(method="ffill", inplace=True)
    df.fillna(method="bfill", inplace=True)

    return df
