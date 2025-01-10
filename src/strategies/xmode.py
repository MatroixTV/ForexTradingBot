import numpy as np
import pandas as pd

class XMode:
    def __init__(self, data, support_resistance_window=14, threshold=0.01):
        """
        XMode initialization.
        :param data: DataFrame containing OHLCV data.
        :param support_resistance_window: Rolling window to calculate support and resistance levels.
        :param threshold: Threshold for identifying breakout levels.
        """
        self.data = data
        self.window = support_resistance_window
        self.threshold = threshold

    def calculate_levels(self):
        """
        Identify support and resistance levels using rolling window logic.
        """
        data = self.data
        data['Support'] = data['Low'].rolling(window=self.window).min()
        data['Resistance'] = data['High'].rolling(window=self.window).max()
        data['XMode_Signal'] = np.where(
            data['Close'] > data['Resistance'] * (1 + self.threshold), 1,
            np.where(data['Close'] < data['Support'] * (1 - self.threshold), -1, 0)
        )
        return data[['Support', 'Resistance', 'XMode_Signal']]
