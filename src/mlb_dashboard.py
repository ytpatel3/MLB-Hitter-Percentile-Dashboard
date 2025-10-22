"""
Yash Patel
mlb_dashboard.py: frontend dashboard
Dataset: https://baseballsavant.mlb.com/leaderboard/percentile-rankings?type=batter&year=2025&team=&sort=1&sortDir=desc
"""

import panel as pn
import plotly.express as px
from mlbapi import MLBAPI

pn.extension(theme='dark')
api = MLBAPI('percentile_rankings.csv')

df = api.get_df()
player_col = api.get_player_name()
metric_cols = api.get_metrics()

# Holoviz Panel searching/filtering Widgets
metric_select = pn.widgets.Select(name='Metric', options=metric_cols, value=metric_cols[0])
min_slider = pn.widgets.FloatSlider(name='Minimum Percentile', start=0, end=100, step=1, value=50)


# callback functions
def make_table(metric, min_val):
    try:
        filtered = api.filter_players(metric, min_val)
    except ValueError as e:
        return pn.pane.Markdown(f'{str(e)}', style={'color': 'red'})
    
    if filtered.empty:
        return pn.pane.Markdown('No players match the filter criteria.', style={'color': 'red'})
    
    table = pn.widgets.Tabulator(
        filtered[[player_col, metric]].sort_values(player_col, ascending=True),
        show_index=False, 
        pagination='remote',
        page_size=10, 
        sizing_mode='stretch_width'
    )
    return table
    
def make_parallel_plot(metric, min_val):
    return

def make_spider_plot(metric, min_val):
    return


# callback bindings
table_panel = pn.bind(make_table, metric_select, min_slider)

# dashboard layout
controls = pn.WidgetBox(
    '# ⚾️ 2025 MLB Regular Season Hitter Percentile Explorer',
    '## by Yash Patel',
    'Use the widgets below to filter and explore hitter performance across percentile metrics.',
    metric_select,
    min_slider,
    width=350,
)

content = pn.Column(
    '## Relevant Players',
    table_panel,
    pn.layout.Divider()
)

dashboard = pn.Row(controls, content)


if __name__ == '__main__':
    pn.serve(dashboard, title='MLB Explorer')
