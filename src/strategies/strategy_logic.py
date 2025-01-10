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

import joblib
import numpy as np
import pandas as pd

class TradingStrategy:
    def __init__(self, df):
        """
        Initializes the trading strategy with a trained model.
        """
        self.df = df
        self.model = joblib.load("trade_decision_model.pkl")
        self.features = ['RSI', 'MACD', 'MACD_Signal', 'RTD_Trend', 'RSI_Squared', 'MACD_Signal_Diff']

    def trading_logic(self, row):
        """
        Makes trade decisions using the trained model.
        """
        # Prepare input features for the model
        feature_values = np.array([row[feature] for feature in self.features]).reshape(1, -1)

        # Predict action: 1 = Buy, -1 = Sell, 0 = No action
        prediction = self.model.predict(feature_values)[0]

        if prediction == 1:
            return "BUY"
        elif prediction == -1:
            return "SELL"
        else:
            return None

    def calculate_confidence(self, row):
        """
        Calculate confidence score for a trade decision.
        Example: Combine RSI, MACD, and RTD metrics into a weighted confidence score.
        """
        try:
            rsi = row["RSI"]
            macd = row["MACD"]
            macd_signal = row["MACD_Signal"]
            rtd_trend = row["RTD_Trend"]

            confidence = 0

            # Weight RSI
            if rsi < self.buy_threshold_rsi:
                confidence += (self.buy_threshold_rsi - rsi) / self.buy_threshold_rsi
            elif rsi > self.sell_threshold_rsi:
                confidence -= (rsi - self.sell_threshold_rsi) / self.sell_threshold_rsi

            # Weight MACD
            confidence += macd - macd_signal

            # Weight RTD Trend
            confidence += rtd_trend

            print(f"Calculated confidence: {confidence}")
            return confidence
        except KeyError as e:
            print(f"Error in calculate_confidence: Missing key {e}")
            return 0
