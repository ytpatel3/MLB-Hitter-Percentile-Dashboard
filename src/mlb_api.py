"""
Yash Patel
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

    def get_df(self):
        """getter function for the dataset"""
        return self.df.copy()
    
    def get_player_name(self):
        """player name used in conjunction with get_metrics for visualizations"""
        player_col = 'player_name' if 'player_name' in self.df.columns else self.df.columns[0]
        return player_col
    
    def get_metrics(self):
        """list of percentile metrics used for visualizations"""
        exclude_cols = {'player_name', 'player_id', 'year'}    
        metrics = [col for col in self.df.columns if col not in exclude_cols]
        return metrics
    
    def filter_players(self, metric, min_val=50):
        """filter for players in the percentile for a specific metric above the min_val"""
        if metric in self.df.columns:
            filtered = self.df[self.df[metric] >= min_val].copy()
            filtered.sort_values(metric, ascending=False)
        else:
            raise ValueError(f'{metric} is not a valid field in the dataset.')

        return filtered
    

if __name__ == '__main__':
    MLBAPI('percentile_rankings.csv')