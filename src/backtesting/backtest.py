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
    """
    Perform backtesting on the DataFrame using the defined strategy logic.
    """
    # Ensure 'Date' is a column and not part of the index
    if "Date" not in df.columns:
        df.reset_index(inplace=True)
        print("Resetting index to include 'Date' as a column.")

    trades = []
    balance = 10000  # Initial balance
    position = None  # Track the current open position
    strategy = TradingStrategy(df)

    for idx, row in df.iterrows():
        action = strategy.trading_logic(row)

        if action == "BUY" and not position:
            print(f"BUY signal triggered at {row['Date']}, price: {row['Close']}")
            position = {"entry_price": row["Close"], "entry_date": row["Date"]}

        elif action == "SELL" and position:
            print(f"SELL signal triggered at {row['Date']}, price: {row['Close']}")
            profit = row["Close"] - position["entry_price"]
            balance += profit
            trades.append({
                "entry_date": position["entry_date"],
                "exit_date": row["Date"],
                "entry_price": position["entry_price"],
                "exit_price": row["Close"],
                "profit": profit,
            })
            position = None

    return trades, balance

if __name__ == "__main__":
    # Load and calculate indicators
    df = pd.read_csv("C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv")
    df = calculate_indicators(df)
    print(df[["RSI", "MACD", "MACD_Signal", "RTD_Trend"]].tail())

    # Run backtest
    trades, final_balance = backtest(df)
    print(f"Total Trades: {len(trades)}")
    print(f"Final Balance: {final_balance:.2f}")
    print("Trades:", trades)



# C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv