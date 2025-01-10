import numpy as np
import pandas as pd

class RTD:
    def __init__(self, data, fast=0.11, slow=0.06):
        """
        RTD initialization.
        :param data: DataFrame containing OHLCV data.
        :param fast: Fast EMA factor for MAMA.
        :param slow: Slow EMA factor for FAMA.
        """
        self.data = data
        self.fast = fast
        self.slow = slow

    def calculate_rtd(self):
        """
        Calculate MAMA and FAMA for RTD and generate trend signals.
        """
        data = self.data
        data['MAMA'], data['FAMA'] = self._calculate_mama_fama(data['Close'], self.fast, self.slow)
        data['RTD_Trend'] = np.where(data['MAMA'] > data['FAMA'], 1, -1)
        return data[['MAMA', 'FAMA', 'RTD_Trend']]

    def _calculate_mama_fama(self, price, fast, slow):
        """
        Calculate MAMA and FAMA based on MESA principles.
        """
        mama = price.ewm(span=int(1 / fast)).mean()
        fama = price.ewm(span=int(1 / slow)).mean()
        return mama, fama
