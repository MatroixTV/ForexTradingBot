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

def backtest(df):
    trades = []
    initial_balance = 10000
    balance = initial_balance
    position = None
    strategy = TradingStrategy(df)  # Pass the DataFrame as an argument

    for index, row in df.iterrows():
        action = strategy.trading_logic(row)
        if action == "BUY" and position is None:
            position = {"entry_price": row["Close"], "entry_date": row["Date"]}
            trades.append({"action": "BUY", "price": row["Close"], "date": row["Date"]})
        elif action == "SELL" and position is not None:
            profit = row["Close"] - position["entry_price"]
            balance += profit
            trades.append({"action": "SELL", "price": row["Close"], "date": row["Date"], "profit": profit})
            position = None

    return trades, balance

if __name__ == "__main__":
    # Load and calculate indicators
    df = pd.read_csv("C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv")
    df = calculate_indicators(df)

    # Run backtest
    trades, final_balance = backtest(df)
    print(f"Total Trades: {len(trades)}")
    print(f"Final Balance: {final_balance:.2f}")
    print("Trades:", trades)



# C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv