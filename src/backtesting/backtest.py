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
from src.indicators.indicators_setup import compute_indicators
import logging


def backtest(data):
    strategy = TradingStrategy()
    trades = []
    balance = 10000  # Starting balance
    position = None
    entry_price = 0

    for index, row in data.iterrows():
        action = strategy.trading_logic(row)
        if action:
            trades.append(action)
            if action["action"] == "BUY" and position != "LONG":
                position = "LONG"
                entry_price = action["price"]
                balance -= entry_price
                print(f"BUY at {entry_price} on {action['date']}")
            elif action["action"] == "SELL" and position == "LONG":
                position = None
                exit_price = action["price"]
                balance += exit_price
                profit = exit_price - entry_price
                print(f"SELL at {exit_price} on {action['date']}, Profit: {profit}")

    # Analyze performance
    analyze_performance(trades, balance)

def analyze_performance(trades, balance):
    if not trades:
        print("No trades executed.")
        return

    profits = [trade["price"] for trade in trades if trade["action"] == "SELL"]
    if profits:
        max_drawdown = max(profits) - min(profits)
        sharpe_ratio = (sum(profits) / len(profits)) / (max_drawdown if max_drawdown != 0 else 1)
    else:
        max_drawdown = 0
        sharpe_ratio = 0

    print(f"Final Balance: {balance}")
    print(f"Sharpe Ratio: {sharpe_ratio}")





# C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv