#### Library import
import pandas as pd
import numpy as np
import streamlit as st
from dash import Dash, dcc, html

#### Default variables

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

# Initiliaze the app
app = Dash(__name__)
app.title = 'NBA Scounting Stats'

# Layout of the app
app.layout = html.Div([
    html.Div(children='NBA Scounting Stats', id='title')
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
