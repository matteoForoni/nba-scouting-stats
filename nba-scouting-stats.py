#### Library import
import pandas as pd
import numpy as np
import streamlit as st
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px

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
    ### Graphs 1
    html.H2(children='Top Players for a specific season', className="paragraphTitle"),
    dcc.Dropdown(np.sort(games_full_df['SEASON'].unique()), '2003', id='season-dropdown'),
    html.Div([ html.P(children='Summed Statistics', className='tableLabel'),
                dash_table.DataTable([], GENERAL_STATS_COLUMNS, id='stats-sum-table',style_table={'border': 'thin lightgrey solid'},
                                                                style_header={'backgroundColor':'lightgrey','fontWeight':'bold'},
                                                                style_cell={'textAlign':'center','width':'12%'})
    ],  className='primary2DivSplit'),
    html.Div([ html.P(children='Averaged Statistics', className='tableLabel'),
                dash_table.DataTable([], GENERAL_STATS_COLUMNS, id='stats-avg-table',style_table={'border': 'thin lightgrey solid'},
                                                                style_header={'backgroundColor':'lightgrey','fontWeight':'bold'},
                                                                style_cell={'textAlign':'center','width':'12%'})
    ],  className='secondary2DivSplit'),
    ### Graphs 2
    html.H2(children='Team statistic for a specific season', className="paragraphTitle"),
    html.P(children='Team Dropdown', className='tableLabel'),
    dcc.Dropdown(np.sort(games_full_df['TEAM'].unique()), 'All', id='team-dropdown'),
    html.P(children='Summed Statistic', className='tableLabel'),
    html.Div([ dcc.Graph(id='pts-team-season-sum')],  
                className='primary2DivSplit'),
    html.Div([ dcc.Graph(id='reb-team-season-sum')],  
                className='secondary2DivSplit'),
    html.Div([ dcc.Graph(id='ast-team-season-sum')],  
                className='primary3DivSplit'),
    html.Div([ dcc.Graph(id='fg3m-team-season-sum')],  
                className='secondary3DivSplit'),
    html.Div([ dcc.Graph(id='fg3a-team-season-sum')],  
                className='secondary3DivSplit'),
    html.P(children='Averaged Statistic', className='tableLabel'),
    html.Div([ dcc.Graph(id='pts-team-season-avg')],  
                className='primary2DivSplit'),
    html.Div([ dcc.Graph(id='reb-team-season-avg')],  
                className='secondary2DivSplit'),
    html.Div([ dcc.Graph(id='ast-team-season-avg')],  
                className='primary3DivSplit'),
    html.Div([ dcc.Graph(id='fg3m-team-season-avg')],  
                className='secondary3DivSplit'),
    html.Div([ dcc.Graph(id='fg3a-team-season-avg')],  
                className='secondary3DivSplit'),
    ### Graphs 3
    html.H2(children='Team statistic divided by players for a specific season', className="paragraphTitle"),
    html.Div([ html.P(children='Season Dropdown', className='tableLabel'),
                dcc.Dropdown(np.sort(games_full_df['SEASON'].unique()), '2003', id='season-dropdown-pie')],  
                className='primary2DivSplit'),
    html.Div([ html.P(children='Team Dropdown', className='tableLabel'),
                dcc.Dropdown(np.sort(games_full_df['TEAM'].unique()), 'Bulls', id='team-dropdown-pie')],  
            className='secondary2DivSplit'), 
    html.Div([ dcc.Graph(id='pts-team-player-pie')],  
                className='primary2DivSplit'),
    html.Div([ dcc.Graph(id='reb-team-player-pie')],  
                className='secondary2DivSplit'),
    html.Div([ dcc.Graph(id='ast-team-player-pie')],  
                className='primary3DivSplit'),
    html.Div([ dcc.Graph(id='fg3m-team-player-pie')],  
                className='secondary3DivSplit'),
    html.Div([ dcc.Graph(id='fg3a-team-player-pie')],  
                className='secondary3DivSplit'), 
    ### Graphs 4
    html.H2(children='Player statistics across all seasons', className="paragraphTitle"),
    html.P(children='Player Dropdown', className='tableLabel'),
    dcc.Dropdown(np.sort(games_full_df['PLAYER_NAME'].unique()), 'Tyson Chandler', id='player-dropdown'),
    html.P(children='Summed Statistic', className='tableLabel'),
    html.Div([ dcc.Graph(id='pts-player-sum')],  
                className='primary2DivSplit'),
    html.Div([ dcc.Graph(id='reb-player-sum')],  
                className='secondary2DivSplit'),
    html.Div([ dcc.Graph(id='ast-player-sum')],  
                className='primary2DivSplit'),
    html.Div([ dcc.Graph(id='fg3-player-sum')],  
                className='secondary2DivSplit'),
    html.P(children='Averaged Statistic', className='tableLabel'),
    html.Div([ dcc.Graph(id='pts-player-avg')],  
                className='primary2DivSplit'),
    html.Div([ dcc.Graph(id='reb-player-avg')],  
                className='secondary2DivSplit'),
    html.Div([ dcc.Graph(id='ast-player-avg')],  
                className='primary2DivSplit'),
    html.Div([ dcc.Graph(id='fg3-player-avg')],  
                className='secondary2DivSplit'),
    ### Graphs 5
    html.H2(children='Player statistics across all matches of a specific season', className="paragraphTitle"),
    html.P(children='Player Dropdown', className='tableLabel'),
    html.Div([ html.P(children='Season Dropdown', className='tableLabel'),
                dcc.Dropdown(np.sort(games_full_df['SEASON'].unique()), '2003', id='season-dropdown-match')],  
                className='primary2DivSplit'),
    html.Div([ html.P(children='Player Dropdown', className='tableLabel'),
                    dcc.Dropdown(np.sort(games_full_df['PLAYER_NAME'].unique()), 'Tyson Chandler', id='player-dropdown-match')],  
            className='secondary2DivSplit'), 
    html.Div([ dcc.Graph(id='shot-player')],  
                className='primary2DivSplit'),
    html.Div([ dcc.Graph(id='fg3-player')],  
                className='secondary2DivSplit'),
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
    performances_by_season_sum = games_full_df.groupby(['SEASON', 'TEAM','PLAYER_NAME'])[['PTS','REB', 'AST', 'FG3M', 'FG3A']].mean().reset_index().round(decimals=2)
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

### Callback for Team statistic for a specific season
@app.callback(
    Output('pts-team-season-sum', 'figure'),
    Output('pts-team-season-avg', 'figure'),
    Output('reb-team-season-sum', 'figure'),
    Output('reb-team-season-avg', 'figure'),
    Output('ast-team-season-sum', 'figure'),
    Output('ast-team-season-avg', 'figure'),
    Output('fg3m-team-season-sum', 'figure'),
    Output('fg3m-team-season-avg', 'figure'),
    Output('fg3a-team-season-sum', 'figure'),
    Output('fg3a-team-season-avg', 'figure'),
    Input('team-dropdown', 'value')
)
def update_graphs(team):
    performances_by_season_sum = games_full_df.groupby(['SEASON', 'TEAM'])[['PTS','REB', 'AST', 'FG3M', 'FG3A' ]].sum().reset_index()
    performances_by_season_avg = games_full_df.groupby(['SEASON', 'TEAM', 'GAME_ID'])[['PTS','REB', 'AST', 'FG3M', 'FG3A']].sum().groupby(['SEASON', 'TEAM']).mean().reset_index()
    if team != 'All':
        plot_sum_data = performances_by_season_sum[performances_by_season_sum['TEAM'] == team]
        plot_avg_data = performances_by_season_avg[performances_by_season_avg['TEAM'] == team]
    else: 
        plot_sum_data = performances_by_season_sum
        plot_avg_data = performances_by_season_avg
    
    fig1 = px.line(plot_sum_data, x='SEASON', y='PTS', markers=True, color="TEAM", color_discrete_sequence=px.colors.qualitative.Dark24, title = 'Total PTS per Season')
    fig2 = px.line(plot_avg_data, x='SEASON', y='PTS', markers=True, color='TEAM', color_discrete_sequence=px.colors.qualitative.Dark24, title = 'Average PTS per Season')
    fig3 = px.line(plot_sum_data, x='SEASON', y='REB', markers=True, color='TEAM', color_discrete_sequence=px.colors.qualitative.Dark24, title = 'Total REB per Season')
    fig4 = px.line(plot_avg_data, x='SEASON', y='REB', markers=True, color='TEAM', color_discrete_sequence=px.colors.qualitative.Dark24, title = 'Average REB per Season')
    fig5 = px.line(plot_sum_data, x='SEASON', y='AST', markers=True, color='TEAM', color_discrete_sequence=px.colors.qualitative.Dark24, title = 'Total AST per Season')
    fig6 = px.line(plot_avg_data, x='SEASON', y='AST', markers=True, color='TEAM', color_discrete_sequence=px.colors.qualitative.Dark24, title = 'Average AST per Season')
    fig7 = px.line(plot_sum_data, x='SEASON', y='FG3M', markers=True, color='TEAM', color_discrete_sequence=px.colors.qualitative.Dark24, title = 'Total FG3M per Season')
    fig8 = px.line(plot_avg_data, x='SEASON', y='FG3M', markers=True, color='TEAM', color_discrete_sequence=px.colors.qualitative.Dark24, title = 'Average FG3M per Season')
    fig9 = px.line(plot_sum_data, x='SEASON', y='FG3A', markers=True, color='TEAM', color_discrete_sequence=px.colors.qualitative.Dark24, title = 'Total FG3A per Season')
    fig10 = px.line(plot_avg_data, x='SEASON', y='FG3A', markers=True, color='TEAM', color_discrete_sequence=px.colors.qualitative.Dark24, title = 'Average FG3A per Season')

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10

### Callback for Player statistic across all seasons
@app.callback(
    Output('pts-team-player-pie', 'figure'),
    Output('reb-team-player-pie', 'figure'),
    Output('ast-team-player-pie', 'figure'),
    Output('fg3m-team-player-pie', 'figure'),
    Output('fg3a-team-player-pie', 'figure'),
    Input('team-dropdown-pie', 'value'),
    Input('season-dropdown-pie', 'value')
)
def update_pies(team, season):
    performances_by_season_sum = games_full_df.groupby(['SEASON', 'TEAM', 'PLAYER_NAME'])[['PTS','REB', 'AST', 'FG3M', 'FG3A' ]].sum().reset_index()
    plot_sum_data = performances_by_season_sum[(performances_by_season_sum['TEAM'] == team) & (performances_by_season_sum['SEASON'] == int(season))]
    #print(plot_sum_data)
    fig1 = px.pie(plot_sum_data, values=plot_sum_data['PTS'], names=plot_sum_data['PLAYER_NAME'], color_discrete_sequence=px.colors.qualitative.Light24, title =f'PTS division for {team} team in season {season}', hole=.3)
    fig2 = px.pie(plot_sum_data, values=plot_sum_data['REB'], names=plot_sum_data['PLAYER_NAME'], color_discrete_sequence=px.colors.qualitative.Light24, title =f'PTS division for {team} team in season {season}', hole=.3)
    fig3 = px.pie(plot_sum_data, values=plot_sum_data['AST'], names=plot_sum_data['PLAYER_NAME'], color_discrete_sequence=px.colors.qualitative.Light24, title =f'PTS division for {team} team in season {season}', hole=.3)
    fig4 = px.pie(plot_sum_data, values=plot_sum_data['FG3M'], names=plot_sum_data['PLAYER_NAME'], color_discrete_sequence=px.colors.qualitative.Light24, title =f'PTS division for {team} team in season {season}', hole=.3)
    fig5 = px.pie(plot_sum_data, values=plot_sum_data['FG3A'], names=plot_sum_data['PLAYER_NAME'], color_discrete_sequence=px.colors.qualitative.Light24, title =f'PTS division for {team} team in season {season}', hole=.3)

    return fig1, fig2, fig3, fig4, fig5

### Callback for Team statistic for a specific season
@app.callback(
    Output('pts-player-sum', 'figure'),
    Output('reb-player-sum', 'figure'),
    Output('ast-player-sum', 'figure'),
    Output('fg3-player-sum', 'figure'),
    Output('pts-player-avg', 'figure'),
    Output('reb-player-avg', 'figure'),
    Output('ast-player-avg', 'figure'),
    Output('fg3-player-avg', 'figure'),
    Input('player-dropdown', 'value')
)
def update_graphs(player):
    performances_by_season_sum = games_full_df.groupby(['SEASON', 'TEAM', 'PLAYER_NAME'])[['PTS','REB', 'AST', 'FG3M', 'FG3A']].sum().reset_index()
    performances_by_season_avg = games_full_df.groupby(['SEASON', 'TEAM', 'PLAYER_NAME'])[['PTS','REB', 'AST', 'FG3M', 'FG3A']].mean().reset_index()
    plot_sum_data = performances_by_season_sum[performances_by_season_sum['PLAYER_NAME'] == player]
    plot_avg_data = performances_by_season_avg[performances_by_season_avg['PLAYER_NAME'] == player]

    fig1 = px.line(plot_sum_data, x='SEASON', y='PTS', markers=True, color_discrete_sequence=px.colors.qualitative.T10, title = f'Total PTS per Season per player {player}')
    fig2 = px.line(plot_sum_data, x='SEASON', y='REB', markers=True, color_discrete_sequence=px.colors.qualitative.T10, title = f'Total REB per Season per player {player}')
    fig3 = px.line(plot_sum_data, x='SEASON', y='AST', markers=True, color_discrete_sequence=px.colors.qualitative.T10, title = f'Total AST per Season per player {player}')
    fig4 = px.line(plot_sum_data, x='SEASON', y=['FG3M', 'FG3A'], markers=True, color_discrete_sequence=px.colors.qualitative.T10, title = f'Total Three Points Shots Stats per Season per player {player}')
    fig5 = px.line(plot_avg_data, x='SEASON', y='PTS', markers=True, color_discrete_sequence=px.colors.qualitative.T10, title = f'Average PTS per Season per player {player}')
    fig6 = px.line(plot_avg_data, x='SEASON', y='REB', markers=True, color_discrete_sequence=px.colors.qualitative.T10, title = f'Average REB per Season per player {player}')
    fig7 = px.line(plot_avg_data, x='SEASON', y='AST', markers=True, color_discrete_sequence=px.colors.qualitative.T10, title = f'Average AST per Season per player {player}')
    fig8 = px.line(plot_avg_data, x='SEASON', y=['FG3M', 'FG3A'], markers=True, color_discrete_sequence=px.colors.qualitative.T10, title = f'Average Three Points Shots Stats per Season per player {player}')

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8

### Callback for Team statistic for a specific season
@app.callback(
    Output('shot-player', 'figure'),
    Output('fg3-player', 'figure'),
    Input('player-dropdown-match', 'value'),
    Input('season-dropdown-match', 'value')
)
def update_players(player, season):
    plot_data = games_full_df[(games_full_df['PLAYER_NAME'] == player) & (games_full_df['SEASON'] == int(season))]
    plot_data['GAME_NUMBER'] = range(len(plot_data))

    fig1 = px.line(plot_data, x='GAME_NUMBER', y=['PTS', 'REB', 'AST'], markers=True, color_discrete_sequence=px.colors.qualitative.Dark24, title = f'PTS, REB and AST per match per season {season} per player {player}')
    fig2 = px.line(plot_data, x='GAME_NUMBER', y=['FG3A', 'FG3M'], markers=True, color_discrete_sequence=px.colors.qualitative.Dark24, title = f'FG3M, FG3A per match per season {season} per player {player}')

    return fig1, fig2


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
