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
        self.position = None  # Track current position (e.g., "BUY", "SELL")

    def trading_logic(self, row):
        """
        Determine trade action based on indicators.
        """
        try:
            rsi = row["RSI"]
            macd = row["MACD"]
            macd_signal = row["MACD_Signal"]
            rtd_trend = row["RTD_Trend"]
            atr = row["ATR"]

            # Compute confidence metric
            confidence = (
                0.3 * (rsi < 30) +  # Oversold
                0.4 * (macd > macd_signal) +  # MACD bullish crossover
                0.3 * (rtd_trend == "BUY")  # RTD trend alignment
            )

            # Dynamic thresholds
            stop_loss = row["Close"] - 1.5 * atr
            take_profit = row["Close"] + 2.0 * atr

            # Decide action based on confidence
            if confidence >= 0.7 and self.position != "BUY":
                self.position = "BUY"
                return {
                    "action": "BUY",
                    "price": row["Close"],
                    "date": row["Date"],
                    "stop_loss": stop_loss,
                    "take_profit": take_profit
                }
            elif confidence <= 0.3 and self.position != "SELL":
                self.position = "SELL"
                return {
                    "action": "SELL",
                    "price": row["Close"],
                    "date": row["Date"],
                    "stop_loss": stop_loss,
                    "take_profit": take_profit
                }

        except Exception as e:
            print(f"Error in trading_logic: {e}")
        return None
