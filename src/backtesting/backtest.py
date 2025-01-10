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


def backtest(df, initial_balance=10000):
    balance = initial_balance
    trades = []
    open_position = None
    strategy = TradingStrategy(confidence_threshold=0.7)  # Adjusted threshold

    for _, row in df.iterrows():
        action = strategy.trading_logic(row)

        if action == "BUY" and open_position is None:
            open_position = {
                "action": "BUY",
                "price": row["Close"],
                "date": row["Date"]
            }
            trades.append(open_position)
            print(f"Executed BUY at {row['Close']} on {row['Date']}")

        elif action == "SELL" and open_position is not None and open_position["action"] == "BUY":
            sell_trade = {
                "action": "SELL",
                "price": row["Close"],
                "date": row["Date"]
            }
            trades.append(sell_trade)
            profit = row["Close"] - open_position["price"]
            balance += profit
            print(f"Executed SELL at {row['Close']} on {row['Date']}. Profit: {profit:.2f}")
            open_position = None

    return trades, balance


if __name__ == "__main__":
    # Load and preprocess data
    df = pd.read_csv("C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv")
    df = calculate_indicators(df)

    # Perform backtest
    trades, final_balance = backtest(df)
    print(f"Total Trades: {len(trades)}")
    print(f"Final Balance: {final_balance:.2f}")
    print(f"Trades: {trades}")


# C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv