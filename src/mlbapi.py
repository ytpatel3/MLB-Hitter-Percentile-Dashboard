"""
Yash Patel
HW3
mlbapi.py: API backend
"""

import pandas as pd

class MLBAPI:

    def __init__(self, path):
        self.df = pd.read_csv(path)
        self._clean_data()

    def _clean_data(self):
        """standardize column names and replace nulls with 0 (0th percentile)"""
        self.df.columns = [col.lower().strip().replace(' ','_') for col in self.df.columns]
        self.df.fillna(0, inplace=True)


if __name__ == '__main__':
    MLBAPI('../percentile_rankings.csv')