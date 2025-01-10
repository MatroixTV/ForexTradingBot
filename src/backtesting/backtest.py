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


def backtest(df, initial_balance=10000):
    """
    Perform backtesting on the provided DataFrame.
    """
    # Initialize strategy and other variables
    df = calculate_indicators(df)
    strategy = TradingStrategy(df)
    balance = initial_balance
    positions = []
    trades = []
    win_count = 0
    loss_count = 0

    print("Starting backtest...")

    for index, row in df.iterrows():
        action = strategy.trading_logic(row)

        if action == "BUY":
            if not positions:
                position = {
                    "entry_price": row["Close"],
                    "entry_date": index,
                    "confidence": strategy.calculate_confidence(row),
                }
                positions.append(position)
                print(f"BUY executed at {position['entry_price']} on {position['entry_date']}")
        elif action == "SELL" and positions:
            entry = positions.pop()
            sell_price = row["Close"]
            profit = sell_price - entry["entry_price"]
            trades.append(
                {
                    "entry_price": entry["entry_price"],
                    "sell_price": sell_price,
                    "entry_date": entry["entry_date"],
                    "sell_date": index,
                    "profit": profit,
                }
            )
            balance += profit
            print(f"SELL executed at {sell_price} on {index}. Profit: {profit:.2f}")

            if profit > 0:
                win_count += 1
            else:
                loss_count += 1

    # Performance Metrics
    total_trades = len(trades)
    win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0
    total_profit = sum(trade["profit"] for trade in trades)
    max_drawdown = calculate_max_drawdown(trades, initial_balance)
    sharpe_ratio = calculate_sharpe_ratio(trades, initial_balance)

    print("\nBacktest Complete!")
    print(f"Final Balance: {balance:.2f}")
    print(f"Total Trades: {total_trades}, Winning Trades: {win_count}, Losing Trades: {loss_count}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Total Profit: {total_profit:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2f}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

    return trades, balance


def calculate_max_drawdown(trades, initial_balance):
    """
    Calculate the maximum drawdown during the backtest.
    """
    balance = initial_balance
    peak_balance = initial_balance
    max_drawdown = 0

    for trade in trades:
        balance += trade["profit"]
        peak_balance = max(peak_balance, balance)
        drawdown = peak_balance - balance
        max_drawdown = max(max_drawdown, drawdown)

    return max_drawdown


def calculate_sharpe_ratio(trades, initial_balance):
    """
    Calculate the Sharpe ratio for the backtest.
    """
    returns = [trade["profit"] / initial_balance for trade in trades]
    if len(returns) < 2:
        return 0
    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
    standard_deviation = variance ** 0.5
    sharpe_ratio = mean_return / standard_deviation if standard_deviation != 0 else 0
    return sharpe_ratio


if __name__ == "__main__":
    # Load your data (replace with your actual data file path)
    file_path = "C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv"
    df = pd.read_csv(file_path)

    # Ensure data is processed correctly
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    # Run the backtest
    trades, final_balance = backtest(df)




# C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv