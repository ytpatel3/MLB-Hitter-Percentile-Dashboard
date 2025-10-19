"""
Yash Patel
HW3
mlbapi.py: API backend
"""

import polars as pl

class MLBAPI:

    def __init__(self, path):
        self.df = pl.read_csv(path)
        self._clean_data()

    def _clean_data(self):
        """standardize column names and replace nulls with 0 (0th percentile)"""
        
        self.df = self.df.rename({col: col.lower().strip().replace(' ','_') for col in self.df.columns})
        self.df = self.df.fill_null(0)



if __name__ == '__main__':
    MLBAPI('../percentile_rankings.csv')