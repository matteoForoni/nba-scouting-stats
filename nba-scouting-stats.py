#### Library import
import pandas as pd
import numpy as np
import streamlit as st
from dash import Dash, dcc, html, Input, Output, callback, dash_table

#### Default variables
EXTERNAL_STYLESHEET = [{
    "href": ('./asset/css/style.css'),
    "rel": "stylesheet",
    "type": "text/css"
}]

GENERAL_STATS_COLUMNS = [
    { 'name': 'STATS TYPE', 'id': '0'},
    { 'name': 'PLAYER', 'id': '1'},
    { 'name': 'TEAM', 'id': '2'},
    { 'name': 'STATS VALUE', 'id': '3'},
]

#### General functions

#### MAIN

# Read data
teams_df = pd.read_csv('./dataset/teams.csv')
games_df = pd.read_csv('./dataset/games.csv')
games_details_df = pd.read_csv('./dataset/games_details.csv')
players_df = pd.read_csv('./dataset/players.csv')
ranking_df = pd.read_csv('./dataset/ranking.csv')

# Data cleaning
## Teams dataset --> fill NaN ARENA CAPACITY values to 0
teams_df['ARENACAPACITY'].fillna(0, inplace=True)
## Games dataset --> drop NaN values
games_df.dropna(inplace=True)
## Game details --> drop NaN values from columns MIN and PLUS_MINUS, set NaN values to N/A in NICKNAME, START_POSITION and COMMENT columns
games_details_df.dropna(subset=['MIN'],inplace=True)
games_details_df['NICKNAME'].fillna('N/A', inplace=True)
games_details_df['START_POSITION'].fillna('N/A', inplace=True)
games_details_df['COMMENT'].fillna('N/A', inplace=True)
games_details_df.dropna(subset=['PLUS_MINUS'], inplace=True)

# Data merge
## Include season information
games_full_df = pd.merge(games_details_df, games_df[['SEASON','GAME_ID']], how='inner', left_on='GAME_ID', right_on='GAME_ID')
games_full_df.rename(columns={'NICKNAME': 'PLAYER_NICKNAME'}, inplace=True)
## Include Teams Nickname
games_full_df = pd.merge(games_full_df, teams_df[['TEAM_ID', 'NICKNAME']], how='inner', left_on='TEAM_ID', right_on='TEAM_ID')
games_full_df.rename(columns={'NICKNAME': 'TEAM'}, inplace=True)

# Data Visualization
### Graph 1 --> For specific season, evaluate top players for pts, reb, assist and fg3


# Initiliaze the app
app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEET)
app.title = 'NBA Scounting Stats'

# Layout of the app
# html.Div(children='NBA Scounting Stats', className='title')
app.layout = html.Div([
    html.H1(children='NBA Scouting Stats', style={'textAlign':'left'}),
    html.H2(children='Top Players for a specific season', className="paragraphTitle"),
    dcc.Dropdown(np.sort(games_full_df['SEASON'].unique()), '2003', id='season-dropdown'),
    html.Div([ html.P(children='Summed Statistics', className='tableLabel'),
                dash_table.DataTable([], GENERAL_STATS_COLUMNS, id='stats-sum-table',style_table={'border': 'thin lightgrey solid'},
                                                                style_header={'backgroundColor':'lightgrey','fontWeight':'bold'},
                                                                style_cell={'textAlign':'center','width':'12%'})
    ],  style={'display': 'inline-block', 'width': '45%', 'margin-left': '5px', 'margin-right': '20px'}),
    html.Div([ html.P(children='Averaged Statistics', className='tableLabel'),
                dash_table.DataTable([], GENERAL_STATS_COLUMNS, id='stats-avg-table',style_table={'border': 'thin lightgrey solid'},
                                                                style_header={'backgroundColor':'lightgrey','fontWeight':'bold'},
                                                                style_cell={'textAlign':'center','width':'12%'})
    ],  style={'display': 'inline-block', 'width': '45%', 'margin-left': '20px'}),

])

### Callback for stats-sum-table
@app.callback(
    Output('stats-sum-table', 'data'),
    Input('season-dropdown', 'value')
)
def update_table(season):
    stats_col = ['PTS','REB', 'AST', 'FG3M', 'FG3A']
    performances_by_season_sum = games_full_df.groupby(['SEASON', 'TEAM','PLAYER_NAME'])[['PTS','REB', 'AST', 'FG3M', 'FG3A']].sum().reset_index()
    #print(type(season))
    season_data_df = performances_by_season_sum[performances_by_season_sum['SEASON'] == int(season)]
    #print(season_data_df)
    table_data = []
    for col in stats_col:
        #print(col)
        best_player = season_data_df[season_data_df[col] == season_data_df[col].max()]
        #print(best_player)
        table_data.append({
            '0': col,
            '1': best_player['PLAYER_NAME'].values[0],
            '2': best_player['TEAM'].values[0],
            '3': season_data_df[col].max()
        })
    #print(table_data)
    return table_data

### Callback for stats-avg-table
@app.callback(
    Output('stats-avg-table', 'data'),
    Input('season-dropdown', 'value')
)
def update_table(season):
    stats_col = ['PTS','REB', 'AST', 'FG3M', 'FG3A']
    performances_by_season_sum = games_full_df.groupby(['SEASON', 'TEAM','PLAYER_NAME'])[['PTS','REB', 'AST', 'FG3M', 'FG3A']].mean().reset_index()
    #print(type(season))
    season_data_df = performances_by_season_sum[performances_by_season_sum['SEASON'] == int(season)]
    #print(season_data_df)
    table_data = []
    for col in stats_col:
        #print(col)
        best_player = season_data_df[season_data_df[col] == season_data_df[col].max()]
        #print(best_player)
        table_data.append({
            '0': col,
            '1': best_player['PLAYER_NAME'].values[0],
            '2': best_player['TEAM'].values[0],
            '3': season_data_df[col].max()
        })
    #print(table_data)
    return table_data

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
