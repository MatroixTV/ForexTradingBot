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
from src.indicators.indicators_setup import calculate_indicators
from src.strategies.strategy_logic import TradingStrategy

def backtest(data):
    """
    Backtests the strategy using the TradingStrategy class.
    """
    strategy = TradingStrategy()
    trades = []
    balance = 10000  # Starting balance
    position = None

    for _, row in data.iterrows():
        signal = strategy.trading_logic(row)

        if signal == "BUY" and position is None:
            position = {"price": row["Close"], "type": "BUY"}
            trades.append({"action": "BUY", "price": row["Close"], "date": row["Date"]})
        elif signal == "SELL" and position and position["type"] == "BUY":
            profit = row["Close"] - position["price"]
            balance += profit
            trades.append({"action": "SELL", "price": row["Close"], "date": row["Date"]})
            position = None

    print(f"Final Balance: {balance}")
    print(f"Trades: {trades}")
    return trades, balance


if __name__ == "__main__":
    # Load and process data
    data_path = "C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv"
    df = pd.read_csv(data_path)
    df = calculate_indicators(df)

    # Run backtest
    trades, final_balance = backtest(df)


# C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv