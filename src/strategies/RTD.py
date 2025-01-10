import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class MESAAlgorithm:
    def __init__(self, source='Close', fast=0.11, slow=0.06):
        self.source = source
        self.fast = fast
        self.slow = slow

    def get_mesa(self, series):
        PI = 3.14159
        alpha = 0.0
        MAMA = np.zeros(len(series))  # Initialize MAMA array
        FAMA = np.zeros(len(series))  # Initialize FAMA array
        Phase = np.zeros(len(series))  # Initialize Phase array
        Period = np.ones(len(series)) * 6  # Default period = 6

        for i in range(6, len(series)):
            # Smooth the data
            smooth = (4 * series[i] + 3 * series[i - 1] + 2 * series[i - 2] + series[i - 3]) / 10
            detrender = (0.0962 * smooth + 0.5769 * smooth - 0.5769 * smooth - 0.0962 * smooth) * (0.075 * Period[i - 1] + 0.54)

            # Calculate in-phase and quadrature components
            Q1 = (0.0962 * detrender + 0.5769 * detrender - 0.5769 * detrender - 0.0962 * detrender) * (0.075 * Period[i - 1] + 0.54)
            I1 = detrender

            jI = (0.0962 * I1 + 0.5769 * I1 - 0.5769 * I1 - 0.0962 * I1) * (0.075 * Period[i - 1] + 0.54)
            jQ = (0.0962 * Q1 + 0.5769 * Q1 - 0.5769 * Q1 - 0.0962 * Q1) * (0.075 * Period[i - 1] + 0.54)

            I2 = I1 - jQ
            Q2 = Q1 + jI
            Re = I2 * I2 + Q2 * Q2
            Im = I2 * Q2 - Q2 * I2

            # Calculate period and phase
            if Im != 0 and Re != 0:
                Period[i] = 2 * PI / np.arctan(Im / Re)
                Phase[i] = 180 / PI * np.arctan(Q1 / I1)

            # Calculate alpha
            alpha = self.fast / max(1, Phase[i] - Phase[i - 1])
            alpha = max(self.slow, min(self.fast, alpha))

            # Calculate MAMA and FAMA
            MAMA[i] = alpha * series[i] + (1 - alpha) * MAMA[i - 1]
            FAMA[i] = 0.5 * alpha * MAMA[i] + (1 - 0.5 * alpha) * FAMA[i - 1]

        return MAMA, FAMA

    def plot_mesa(self, data, MAMA, FAMA):
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['Close'], label='Price')  # Ensure alignment with index
        plt.plot(data.index, MAMA, label='MAMA', color='green')
        plt.plot(data.index, FAMA, label='FAMA', color='red')
        plt.legend()
        plt.title('MESA Adaptive Moving Average')
        plt.show()

    def run(self, data):
        # Filter out invalid dates and ensure correct alignment
        series = data[self.source].values  # Extract Close prices
        MAMA, FAMA = self.get_mesa(series)  # Compute indicators
        self.plot_mesa(data, MAMA, FAMA)  # Plot results

def check_rtd_trend(data):
    """
    Check the trend based on the close prices.
    Returns 'uptrend' if the last close is higher than the previous one, 'downtrend' otherwise.
    """
    if isinstance(data, pd.Series):  # If it's a single row (pandas Series)
        if data['Close'] > data['Close']:
            return "uptrend"
        else:
            return "downtrend"
    else:  # If it's a DataFrame
        return "uptrend" if data['Close'].iloc[-1] > data['Close'].iloc[-2] else "downtrend"


# Example usage
if __name__ == "__main__":
    # Load sample data
    data = pd.read_csv('C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv')

    # Print raw data info
    print("Raw Data Info:")
    print(data.head())
    print(data.tail())
    print(data.columns)

    # Ensure 'Date' is parsed correctly
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Handle invalid dates
    data = data.dropna(subset=['Date'])  # Drop invalid dates

    # Filter dates
    data = data[data['Date'] > '1980-01-01']  # Ensure no invalid dates
    print("Filtered Date Range:", data['Date'].min(), "to", data['Date'].max())

    # Set 'Date' as index
    data.set_index('Date', inplace=True)

    # Instantiate and run MESA Algorithm
    mesa = MESAAlgorithm()
    mesa.run(data)


def calculate_rtd_signals(row):
    # Example signal logic
    if row["RTD_Trend"] == "UP":
        return "UP"
    elif row["RTD_Trend"] == "DOWN":
        return "DOWN"
    else:
        return "HOLD"
