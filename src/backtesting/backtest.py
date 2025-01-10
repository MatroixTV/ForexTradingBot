# import pandas as pd
# import numpy as np
# from src.strategies.strategy_logic import trading_logic
# from src.indicators.indicators_setup import add_indicators  # Ensure this import exists
#
# def backtest(data):
#     initial_balance = 10000
#     balance = initial_balance
#     position = None
#
#     for index, row in data.iterrows():
#         if row["Buy_Signal"] and position is None:
#             position = row["Close"]
#             print(f"Buy at {position:.2f}")
#         elif row["Sell_Signal"] and position is not None:
#             profit = row["Close"] - position
#             balance += profit
#             print(f"Sell at {row['Close']:.2f}")
#             position = None
#
#     return balance
#
#
# # Example usage (replace with your dataset loading logic)
# data = pd.read_csv("C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv")
# data = add_indicators(data)  # Ensure this function works correctly
# final_balance = backtest(data)
#


import pandas as pd
from src.strategies.strategy_logic import TradingStrategy
from src.indicators.indicators_setup import calculate_indicators

class Backtester:
    def __init__(self, initial_balance=10000):
        self.balance = initial_balance
        self.trades = []

    def log_trade(self, action, price, date):
        self.trades.append({"action": action, "price": price, "date": date})
        print(f"Trade executed: {action} at {price} on {date}")

    def backtest(self, df):
        strategy = TradingStrategy()
        for _, row in df.iterrows():
            signal = strategy.trading_logic(row)
            if signal == "BUY":
                self.log_trade("BUY", row["Close"], row["Date"])
            elif signal == "SELL":
                self.log_trade("SELL", row["Close"], row["Date"])
        return self.trades, self.balance

    def analyze_performance(self):
        print(f"Final Balance: {self.balance}")
        print(f"Total Trades: {len(self.trades)}")
        print(f"Trades: {self.trades}")

if __name__ == "__main__":
    # Load data
    data_path = "C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv"
    df = pd.read_csv(data_path)

    # Calculate indicators
    df = calculate_indicators(df)

    # Initialize backtester
    backtester = Backtester()

    # Run backtest
    trades, final_balance = backtester.backtest(df)

    # Analyze performance
    backtester.analyze_performance()


# C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv