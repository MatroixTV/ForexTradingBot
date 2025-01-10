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
    def __init__(self, confidence_threshold=0.8):
        self.confidence_threshold = confidence_threshold

    def calculate_confidence(self, row):
        # Ensure numeric comparison
        try:
            confidence = 0
            if pd.to_numeric(row["RSI"], errors="coerce") < 40 or pd.to_numeric(row["RSI"], errors="coerce") > 60:
                confidence += 0.3
            if pd.to_numeric(row["MACD"], errors="coerce") > pd.to_numeric(row["MACD_Signal"], errors="coerce"):
                confidence += 0.3
            if pd.to_numeric(row["RTD_Trend"], errors="coerce") > 0:
                confidence += 0.4
            return confidence
        except (KeyError, TypeError, ValueError) as e:
            print(f"Error in calculate_confidence: {e}")
            return 0  # Return zero confidence for invalid rows

    def trading_logic(self, row):
        try:
            # Extract indicators
            rsi = row["RSI"]
            macd = row["MACD"]
            macd_signal = row["MACD_Signal"]
            rtd_trend = row["RTD_Trend"]

            # Calculate confidence
            confidence = self.calculate_confidence(row)

            # Debugging metrics
            print(f"RSI: {rsi}, MACD: {macd}, MACD_Signal: {macd_signal}, RTD_Trend: {rtd_trend}")
            print(f"Confidence: {confidence}")

            # Determine actions
            if confidence >= self.confidence_threshold:
                if macd > macd_signal and rtd_trend > 0:
                    return "BUY"
                elif macd < macd_signal and rtd_trend < 0:
                    return "SELL"

            return "HOLD"  # Default action
        except KeyError as e:
            print(f"Error in trading_logic: Missing column {e}")
            return "HOLD"
