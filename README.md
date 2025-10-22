#  Hitter Percentile Rankings Dashboard (2025 MLB Regular Season)

## What this project contains
- A reproducible backend that ingests hitter stat percentile data
- An interactive dashboard to explore player-level hitter percentile summaries

## Dataset
Dataset: https://baseballsavant.mlb.com/leaderboard/percentile-rankings?type=batter&year=2025&team=&sort=1&sortDir=desc
Fields included: xwoba, xba, xslg, xiso, xobp, brl, brl_percent, exit_velocity, max_ev, hard_hit_percent, k_percent, bb_percent, whiff_percent, chase_percent, arm_strength, sprint_speed, oaa, bat_speed, squared_up_rate, swing_length

## Dashbaord Visualizations
### 1. Parallel Coordinates Plot
- Purpose: Compare multiple offensive skills at once.
- Metrics: exit_velocity (raw contact quality), k_percent (contact consistency), bb_percent (plate discipline)
- Insight: Shows how hitters balance power, contact, and discipline. Helps identify well-rounded hitters versus specialists (e.g., high-power sluggers with low discipline).

### 2. Swing Mechanics Spider Plot
- Purpose: Visualize the mechanical profile of hitters.
- Metrics: bat_speed, swing_length, squared_up_rate
- Insight: Reveals swing style differences: short, efficient swings vs. long, powerful swings. Useful for spotting players’ mechanical strengths and potential areas for adjustment.

## Key libraries (backend and dashboard)
- Python 3.8+ (recommended)
- pandas — data loading & manipulation
- plotly — plotting library used by the dashboard
- panel — interactive dashboard framework

## Quick start (local)
1. Clone the repo:
   git clone https://github.com/ytpatel3/MLB-RS-2025-Hitter-Percentile-Rankings.git
2. Create and activate a virtual environment:
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows (PowerShell)
3. Install dependencies:
   pip install pandas plotly panel
4. Prepare your data:
   - Place your CSV in the expected data/ folder
5. Run the dashboard:
   python mlb_dashboard.py
   - The dashboard will launch at http://localhost:63019


## Contributing
Contributions are welcome. Please open an issue or a pull request with proposed changes. Include sample data or a data schema if adding new processing logic.
## Contact
Maintainer: ytpatel3 (GitHub)
For questions or help reproducing the dashboard locally, open an issue in this repository.
