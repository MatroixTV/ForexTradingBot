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


def analyze_performance(trades, final_balance, initial_balance):
    """Calculate and log performance metrics."""
    total_trades = len(trades)
    profit_trades = [t for t in trades if t['action'] == 'SELL' and t['profit'] > 0]
    loss_trades = [t for t in trades if t['action'] == 'SELL' and t['profit'] <= 0]

    win_rate = len(profit_trades) / total_trades * 100 if total_trades > 0 else 0
    total_profit = sum([t['profit'] for t in profit_trades])
    total_loss = sum([t['profit'] for t in loss_trades])

    print(f"Total Trades: {total_trades}")
    print(f"Winning Trades: {len(profit_trades)}, Win Rate: {win_rate:.2f}%")
    print(f"Profit: {total_profit:.2f}, Loss: {total_loss:.2f}")
    print(f"Final Balance: {final_balance:.2f}, P/L: {final_balance - initial_balance:.2f}")


def backtest(data):
    """Run the backtesting simulation."""
    initial_balance = 10000
    balance = initial_balance
    trades = []

    strategy = TradingStrategy()

    for index, row in data.iterrows():
        action, confidence = strategy.trading_logic(row)
        print(f"Row {index} Action: {action}, Confidence: {confidence}")

        if action == 'BUY':
            trades.append({'action': 'BUY', 'price': row['Close'], 'date': row['Date'], 'confidence': confidence})
        elif action == 'SELL' and trades:
            buy_trade = trades.pop()
            profit = row['Close'] - buy_trade['price']
            balance += profit
            trades.append({
                'action': 'SELL',
                'price': row['Close'],
                'date': row['Date'],
                'profit': profit,
                'confidence': confidence
            })

    analyze_performance(trades, balance, initial_balance)
    return trades, balance



if __name__ == "__main__":
    file_path = "C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv"
    df = pd.read_csv(file_path)
    df = calculate_indicators(df)
    trades, final_balance = backtest(df)




# C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv