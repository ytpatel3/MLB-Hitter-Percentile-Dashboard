"""
Yash Patel
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

    def get_df(self):
        """getter function for the dataset"""
        return self.df.to_pandas().copy()
    
    def get_player_name(self):
        """player name used in conjunction with get_metrics for visualizations"""
        player_col = 'player_name' if 'player_name' in self.df.columns else self.df.columns[0]
        return player_col.to_pandas()
    
    def get_metrics(self):
        """list of percentile metrics used for visualizations"""
        exclude_cols = {'player_name', 'player_id', 'year'}    
        metrics = self.df[[col for col in self.df.columns if col not in exclude_cols]]
        return metrics.to_pandas()
    
    def filter_players(self, metric, min_val=50):
        """filter for players in the percentile for a specific metric above the min_val"""
        if metric in self.df.columns:
            filtered = self.df.filter(pl.col(metric) >= min_val)
            filtered = filtered.sort(metric, reverse=True)
        else:
            raise ValueError(f'{metric} is not a valid field in the dataset.')

        return filtered.to_pandas()
    

if __name__ == '__main__':
    MLBAPI('percentile_rankings.csv')