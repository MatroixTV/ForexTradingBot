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
from src.strategies.xmode import calculate_xmode_signals
from src.strategies.MAW import calculate_maw_signals
from src.strategies.RTD import calculate_rtd_signals
import logging

class TradingStrategy:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.logger.addHandler(handler)

    def trading_logic(self, row):
        try:
            # Extract indicator values
            rsi = row['RSI']
            macd = row['MACD']
            macd_signal = row['MACD_Signal']
            rtd_trend = row['RTD_Trend']

            # Debug logs for indicator values
            self.logger.debug(f"RSI: {rsi}, MACD: {macd}, MACD_Signal: {macd_signal}, RTD_Trend: {rtd_trend}")

            # Relaxed trading conditions
            if pd.isna(rsi) or pd.isna(macd) or pd.isna(macd_signal) or pd.isna(rtd_trend):
                self.logger.debug("Skipped row due to missing indicator values.")
                return None

            # Buy condition
            if rsi < 30 and macd > macd_signal and rtd_trend > 0:
                self.logger.debug("BUY signal triggered.")
                return "BUY"

            # Sell condition
            if rsi > 70 and macd < macd_signal and rtd_trend < 0:
                self.logger.debug("SELL signal triggered.")
                return "SELL"

            self.logger.debug("No trade conditions met.")
            return None
        except Exception as e:
            self.logger.error(f"Error in trading_logic: {e}")
            return None
