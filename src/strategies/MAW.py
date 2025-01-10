import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MAWAlgorithm:
    def __init__(self, source='Close', period_maw=1111, period_ss=444, post_smooth=11, upper_level=100, lower_level=-100):
        self.source = source
        self.period_maw = period_maw
        self.period_ss = period_ss
        self.post_smooth = post_smooth
        self.upper_level = upper_level
        self.lower_level = lower_level

    def super_smoother(self, series, ss_period):
        sqrt2_pi = np.sqrt(8.0) * np.arcsin(1.0)
        alpha = sqrt2_pi / ss_period
        beta = np.exp(-alpha)
        gamma = -beta * beta
        delta = 2.0 * beta * np.cos(alpha)

        super_smooth = np.zeros(len(series))
        for i in range(2, len(series)):
            super_smooth[i] = (1.0 - delta - gamma) * (series[i] + series[i-1]) * 0.5 \
                              + delta * super_smooth[i-1] + gamma * super_smooth[i-2]
        return super_smooth

    def calculate_maw(self, data):
        series = data[self.source].values
        super_smooth = self.super_smoother(series, self.period_ss)
        slope = (super_smooth[:-self.period_maw] - super_smooth[self.period_maw:]) / self.period_maw
        epsilon = np.zeros(len(series))
        for i in range(len(series)):
            epsilon[i] = np.mean(super_smooth[i:i+self.period_maw] + np.arange(self.period_maw) * slope[i])

        zeta = 2.0 / (self.post_smooth + 1.0)
        ema = np.zeros(len(series))
        for i in range(1, len(series)):
            ema[i] = zeta * epsilon[i] ** 2 + (1.0 - zeta) * ema[i-1]

        raw_output = np.where(ema == 0, 0.0, epsilon / np.sqrt(ema))
        max_maw = pd.Series(raw_output).rolling(self.period_maw).max()
        min_maw = pd.Series(raw_output).rolling(self.period_maw).min()

        scaled_output = 200 * (raw_output - min_maw) / (max_maw - min_maw) - 100
        return scaled_output

    def plot_maw(self, data, scaled_output):
        plt.figure(figsize=(12, 6))
        plt.plot(data['Close'], label='Price', alpha=0.5)
        plt.plot(scaled_output, label='MAW Oscillator', color='orange')
        plt.axhline(self.upper_level, color='red', linestyle='--', label='Upper Threshold')
        plt.axhline(self.lower_level, color='green', linestyle='--', label='Lower Threshold')
        plt.axhline(0, color='gray', linestyle='-', label='Zero Line')
        plt.legend()
        plt.title('Momentum Adaptive Wave (MAW) Oscillator')
        plt.show()

    def run(self, data):
        scaled_output = self.calculate_maw(data)
        self.plot_maw(data, scaled_output)

def check_maw(data):
    # Ensure the data passed is a pandas Series or DataFrame
    if not isinstance(data, (pd.Series, pd.DataFrame)):
        raise ValueError("Invalid data format. Expected pandas DataFrame or Series.")

    # Assuming the 'Close' column exists in the data
    rolling_mean = data['Close'].rolling(window=50).mean()
    # You can now use `rolling_mean` in the rest of the logic
    # For example, you might want to check if it's above/below some threshold
    if rolling_mean.iloc[-1] > data['Close'].iloc[-1]:
        return True  # or some other logic
    return False

def calculate_maw_signals(row):
    # Example signal logic
    if row["MACD"] > row["MACD_Signal"]:
        return "CONFIRM"
    else:
        return "HOLD"

