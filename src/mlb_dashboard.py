"""
Yash Patel
mlb_dashboard.py: frontend dashboard
Dataset: https://baseballsavant.mlb.com/leaderboard/percentile-rankings?type=batter&year=2025&team=&sort=1&sortDir=desc
"""

import panel as pn
import plotly.express as px
from mlb_api import MLBAPI

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
    try: 
        filtered = api.filter_players(metric, min_val)
    except ValueError as e:
        return pn.pane.Markdown(f'{str(e)}', style={'color': 'red'})
    
    if filtered.empty:
        return pn.pane.Markdown('No players match the filter criteria.', style={'color': 'red'})
    
    # Dimensions:
    # 1. exit_velo --> Raw Contact Quality
    # 2. k_percent --> Contact Consistency
    # 3. bb_percent --> Plate Discipline
    # A good metric filter for this plot would be xwOBA. 
    
    fig = px.parallel_coordinates(
        filtered,
        dimensions=['exit_velocity', 'k_percent', 'bb_percent'],
        color=metric, 
        color_continuous_scale=px.colors.diverging.RdBu,
        title=f'Parallel Coordinates of Hitter Stat Percentiles (Filtered by {metric} ≥ {min_val})'
    )
    fig.update_layout(showlegend=True)

    return pn.pane.Plotly(fig, config={'displayModeBar': False})

def make_spider_plot(metric, min_val):
    try: 
        filtered = api.filter_players(metric, min_val)
    except ValueError as e:
        return pn.pane.Markdown(f'{str(e)}', style={'color': 'red'})
    
    if filtered.empty:
        return pn.pane.Markdown('No players match the filter criteria', style={'color': 'red'})
    
    # Dimensions:
    # 1. bat_speed —-> how fast the bat moves
    # 2. swing_length —-> how long/compact the swing is
    # 3. squared_up_rate —-> how often the hitter makes pure contact
    # Insights:
    # Shows the mechanical identity of a hitter — for example,
    # · short, efficient swing guys (high squared_up, low swing_length, moderate bat_speed)
    # · long, explosive swing sluggers (high bat_speed, high swing_length, variable squared_up)
    
    melted = filtered.melt(id_vars=player_col, value_vars=['bat_speed','swing_length','squared_up_rate'], var_name='Metric', value_name='Percentile')
    fig = px.line_polar(
        melted, 
        r='Percentile',
        theta='Metric',
        color=player_col,
        line_close=True,
        title=f'Swing Mechanics Spider Plot (Filtered by {metric} ≥ {min_val})',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_traces(fill='toself', opacity=0.6)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(range=[0,100], tickvals=[0,25,50,75,100])
        ),
        showlegend = True
    )

    return pn.pane.Plotly(fig, config={'displayModeBar': False})



# callback bindings
table_panel = pn.bind(make_table, metric_select, min_slider)
parallel_panel = pn.bind(make_parallel_plot, metric_select, min_slider)
spider_panel = pn.bind(make_spider_plot, metric_select, min_slider)

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
    pn.layout.Divider(),
    parallel_panel,
    pn.layout.Divider(),
    spider_panel,
    pn.layout.Divider()
)

dashboard = pn.Row(controls, content)


if __name__ == '__main__':
    pn.serve(dashboard, title='MLB Explorer')
