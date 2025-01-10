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


import pandas as pd


class TradingStrategy:
    def __init__(self):
        self.previous_signal = None

    def calculate_confidence(self, row):
        # Confidence based on RTD, MACD, and RSI
        confidence = 0
        if row["RTD_Trend"] > 0:
            confidence += 0.4
        if row["MACD"] > row["MACD_Signal"]:
            confidence += 0.3
        if 30 < row["RSI"] < 70:
            confidence += 0.3
        return confidence

    def trading_logic(self, row):
        try:
            confidence = self.calculate_confidence(row)
            print(f"Confidence: {confidence}, RTD_Trend: {row['RTD_Trend']}, RSI: {row['RSI']}, MACD: {row['MACD']}")

            if confidence >= 0.6:
                if self.previous_signal != "BUY":
                    self.previous_signal = "BUY"
                    return "BUY"
            elif confidence <= 0.4:
                if self.previous_signal != "SELL":
                    self.previous_signal = "SELL"
                    return "SELL"
            return None
        except Exception as e:
            print(f"Error in trading_logic: {e}")
            return None
