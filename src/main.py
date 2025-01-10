import pandas as pd
from src.indicators.indicators_setup import add_indicators
from src.strategies.strategy_logic import TradingStrategy
from src.backtesting.backtest import backtest

# Load data
data = pd.read_csv("C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv")

# Add indicators
data = add_indicators(data)

# Generate trading signals
data = TradingStrategy(data)

# Run backtest
final_balance = backtest(data)
print(f"Final Balance: ${final_balance:.2f}")
