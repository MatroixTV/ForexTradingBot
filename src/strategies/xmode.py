import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class XModeAlgorithm:
    def __init__(self, lookbacks=[128, 32, 16, 8]):
        self.lookbacks = lookbacks

    def calculate_levels(self, high, low, lookback):
        # Ensure 'high' and 'low' are pandas Series
        high = pd.Series(high)
        low = pd.Series(low)

        v_low = low.rolling(window=lookback).min()
        v_high = high.rolling(window=lookback).max()
        v_dist = v_high - v_low

        tmp_high = np.where(v_low < 0, 0 - v_low, v_high)
        tmp_low = np.where(v_low < 0, 0 - v_low - v_dist, v_low)

        sf_var = np.log(0.4 * tmp_high) / np.log(10)
        SR = np.where(tmp_high > 25, np.exp(np.log(10) * (np.floor(sf_var) + 1)),
                      100 * np.exp(np.log(8) * np.floor(np.log(0.005 * tmp_high) / np.log(8))))

        N = np.floor(np.log(SR / (tmp_high - tmp_low)) / np.log(8))
        SI = SR * np.exp(-N * np.log(8))
        M = np.floor(np.log((tmp_high - tmp_low) / SI) / np.log(2))
        I = np.round((tmp_high + tmp_low) * 0.5 / (SI * np.exp((M - 1) * np.log(2))))

        Bot = (I - 1) * SI * np.exp((M - 1) * np.log(2))
        Top = (I + 1) * SI * np.exp((M - 1) * np.log(2))

        Increment = (Top - Bot) / 8
        absTop = Top + 3 * Increment

        # Return levels as a pandas Series
        levels = {
            'Plus28': absTop - Increment,
            'Plus18': absTop - 2 * Increment,
            'EightEight': absTop - 3 * Increment,
            'FiveEight': absTop - 6 * Increment,
            'FourEight': absTop - 7 * Increment,
            'ThreeEight': absTop - 8 * Increment,
            'ZeroEight': absTop - 11 * Increment,
            'Minus18': absTop - 12 * Increment,
            'Minus28': absTop - 13 * Increment
        }

        return levels

    def plot_levels(self, data, levels, label):
        plt.figure(figsize=(12, 6))
        plt.plot(data['Close'], label='Price')
        for level_name, level_value in levels.items():
            plt.axhline(y=level_value, linestyle='--', label=f'{label} - {level_name}')
        plt.title(f'Murrey Math Levels - {label}')
        plt.legend()
        plt.show()

    def run(self, data):
        for lookback in self.lookbacks:
            levels = self.calculate_levels(data['High'], data['Low'], lookback)
            self.plot_levels(data, levels, label=f'Lookback {lookback}')


# x_mode_check function for generating trading signals based on the levels
def x_mode_check(dataframe):
    """
    This function checks whether the required columns exist in the dataframe.
    It should be applied to the entire dataframe, not just a row.
    """
    # Define the required columns
    required_columns = ['High', 'Low', 'Close']  # Make sure these columns exist

    # Check if all required columns exist in the dataframe
    if not all(col in dataframe.columns for col in required_columns):
        print(f"Missing columns: {[col for col in required_columns if col not in dataframe.columns]}")
        return False  # If columns are missing, return False

    print("All required columns are present")

    # Proceed with additional checks or logic as per your strategy
    # Example: Check if the latest data meets the desired criteria
    latest_data = dataframe.iloc[-1]  # Access the latest row (most recent data)

    # Example condition: Check if Close price is greater than some threshold
    if latest_data['Close'] > 1.038:
        print(f"Price condition met: {latest_data['Close']} > 1.038")
        return True  # This could be based on any condition you want to set

    print(f"No signal: Price {latest_data['Close']} within range")
    return False  # If no signal, return False


def calculate_xmode_signals(row):
    # Example signal logic
    if row["Close"] > row["BB_Upper"]:
        return "SELL"
    elif row["Close"] < row["BB_Lower"]:
        return "BUY"
    else:
        return "HOLD"
