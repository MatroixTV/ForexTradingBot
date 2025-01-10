# # Updated strategy_logic.py
# import pandas as pd
# import numpy as np
#
# class TradingStrategy:
#     def generate_signals(df):
#         df["Buy_Signal"] = (df["RSI"] < 40) & (df["MACD"] > df["MACD_Signal"]) & (df["Close"] < df["BB_Lower"])
#         df["Sell_Signal"] = (df["RSI"] > 60) & (df["MACD"] < df["MACD_Signal"]) & (df["Close"] > df["BB_Upper"])
#         return df
#
#     def __init__(self, data_row, full_data):
#         self.data_row = data_row
#         self.full_data = full_data
#
#     def stop_loss_take_profit(self, buy_price, risk_ratio=1.5):
#         atr = self.data_row['ATR']
#         stop_loss = buy_price - (atr * risk_ratio)
#         take_profit = buy_price + (atr * risk_ratio)
#         return stop_loss, take_profit
#
#
# # Example usage within backtest logic
#
#
# def trading_logic(row, data):
#     signal = None
#     sl = None  # Stop Loss
#     tp = None  # Take Profit
#
#     # Example conditions using RSI, MACD, and XMODE
#     if row["RSI"] < 30 and row["XMODE"] > 0.7:  # Example XMODE threshold
#         signal = "Buy"
#         sl = row["Close"] * 0.99  # Example Stop Loss at 1% below entry
#         tp = row["Close"] * 1.02  # Example Take Profit at 2% above entry
#     elif row["RSI"] > 70 and row["XMODE"] < -0.7:  # Example XMODE threshold
#         signal = "Sell"
#         sl = row["Close"] * 1.01  # Example Stop Loss at 1% above entry
#         tp = row["Close"] * 0.98  # Example Take Profit at 2% below entry
#
#     return signal, sl, tp


import numpy as np


class TradingStrategy:
    def __init__(self, df):
        """
        Initialize TradingStrategy with the DataFrame containing indicators.
        :param df: DataFrame with calculated indicators.
        """
        self.df = df

    def trading_logic(self, row):
        """
        Define trading logic using indicators and signals.
        :param row: Single row of DataFrame.
        :return: Signal ('BUY', 'SELL', or None).
        """
        try:
            rsi, macd, macd_signal = row['RSI'], row['MACD'], row['MACD_Signal']
            xmode_signal, rtd_trend, maw_oscillator = row['XMode_Signal'], row['RTD_Trend'], row['MAW_Oscillator']

            # Example trading logic
            if xmode_signal == 1 and rtd_trend > 0 and maw_oscillator > 1:
                return 'BUY'
            elif xmode_signal == -1 and rtd_trend < 0 and maw_oscillator < -1:
                return 'SELL'
        except Exception as e:
            print(f"Error in trading_logic: {e}")
        return None

    def calculate_confidence(self, row):
        """
        Calculate confidence for a trade based on multiple indicators.
        :param row: Single row of DataFrame.
        :return: Confidence score.
        """
        confidence = 0
        try:
            if row['RTD_Trend'] > 0:  # Favorable RTD trend
                confidence += 0.4
            if row['XMode_Signal'] != 0:  # XMode Signal present
                confidence += 0.3
            if abs(row['MAW_Oscillator']) > 1:  # Significant MAW Oscillation
                confidence += 0.3
        except Exception as e:
            print(f"Error in calculate_confidence: {e}")
        return confidence
