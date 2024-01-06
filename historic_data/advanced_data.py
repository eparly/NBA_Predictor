from nba_api.stats.endpoints import BoxScoreAdvancedV2, LeagueGameLog, LeagueDashTeamStats, LeagueGameFinder
import pandas as pd
import pickle
import time as t

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

import seaborn as sns
import matplotlib.pyplot as plt

from nba_api.stats.static import teams
def teamID(teamname, teams):

    teams = teams.get_teams()
    ID = [x for x in teams if x['full_name'] == teamname][0]
    ID = ID['id']
    return ID


def store_game_data():
    game_ids_18 = LeagueGameLog(season='2018').get_data_frames()[0]
    game_ids_19 = LeagueGameLog(season='2019').get_data_frames()[0]
    game_ids_20 = LeagueGameLog(season='2020').get_data_frames()[0]
    game_ids_21 = LeagueGameLog(season='2021').get_data_frames()[0]
    game_ids_22 = LeagueGameLog(season='2022').get_data_frames()[0]
    game_ids_23 = LeagueGameLog(season='2023').get_data_frames()[0]

    #combine all game_id dataframes
    game_data = game_ids_18.append(game_ids_19)
    game_data = game_data.append(game_ids_20)
    game_data = game_data.append(game_ids_21)
    game_data = game_data.append(game_ids_22)
    game_data = game_data.append(game_ids_23)

    with open('game_data_18_23.pkl', 'wb') as f:
        pickle.dump(game_data, f)

def get_game_data():
    with open('game_data_18_23.pkl', 'rb') as f:
        game_data = pickle.load(f)
    return game_data


def get_stats():
    all_games = LeagueGameFinder(
        league_id_nullable='00')


    games = all_games.get_data_frames()[0]
    games = games[games.SEASON_ID.str[-4:] >= '2018']
    games = games.dropna(axis='rows')

    games["HOME"] = games.loc[games["MATCHUP"].str.contains(
        '@'), "MATCHUP"].apply(lambda x: 0)
    games["HOME"] = games["HOME"].fillna(1)

    games = games.drop(columns=['SEASON_ID', 'TEAM_ABBREVIATION',
                    'TEAM_NAME', 'GAME_DATE', 'MATCHUP', 'MIN'])

    game_data = get_game_data()
    all_games_stats = pd.DataFrame()
    for game_id in game_data['GAME_ID'].unique():
        #historical data
        single_game_data = games[games['GAME_ID'] == game_id]
        if(len(single_game_data) == 0):
            continue
        
        try:
            data = BoxScoreAdvancedV2(game_id=game_id).get_data_frames()[1]
        except:
            continue
        t.sleep(0.6)

        # Merge 'data' and 'single_game_data' on 'TEAM_ID'
        data = pd.merge(data, single_game_data[['TEAM_ID', 'WL', 'HOME']], on='TEAM_ID', how='left')
        # Split 'data' into two DataFrames for home and away teams
        home_team_data = data[data['HOME'] == 1]
        away_team_data = data[data['HOME'] == 0]

        # Rename columns with 'home_' and 'away_' prefix
        home_team_data.columns = 'HOME_' + home_team_data.columns
        away_team_data.columns = 'AWAY_' + away_team_data.columns

        # Reset index before joining
        home_team_data.reset_index(drop=True, inplace=True)
        away_team_data.reset_index(drop=True, inplace=True)

        # Concatenate along the columns axis
        data = pd.concat([home_team_data, away_team_data], axis=1)
        all_games_stats = all_games_stats.append(data)
    return all_games_stats
        
# data = get_stats()
# with open('all_data.pkl', 'wb') as f:
#         pickle.dump(data, f)

with open('all_data.pkl', 'rb') as f:
        data = pickle.load(f)


a=0

def train(data):
    y = data['HOME_WL']
    #drop the 'AWAY_WL' column because it is the same as 'HOME_WL'
    # data['HOME_WL'] = data['HOME_WL'].map({'W': 1, 'L': 0})
    X = data.drop(
        columns=['HOME_WL', 'AWAY_WL','HOME_GAME_ID', 'AWAY_GAME_ID', 'HOME_TEAM_ID', 'AWAY_TEAM_ID', 
                 'HOME_TEAM_NAME', 'HOME_TEAM_ABBREVIATION', 'HOME_TEAM_CITY', 
                 'HOME_USG_PCT', 'HOME_MIN', 'HOME_HOME', 'AWAY_TEAM_NAME', 'AWAY_TEAM_ABBREVIATION', 
                 'AWAY_TEAM_CITY', 'AWAY_USG_PCT', 'AWAY_MIN', 'AWAY_HOME', 
                 'HOME_E_OFF_RATING', 'HOME_OFF_RATING', 'HOME_E_DEF_RATING', 'HOME_DEF_RATING',
                 'HOME_E_NET_RATING', 'HOME_NET_RATING', 'AWAY_E_OFF_RATING', 'AWAY_OFF_RATING',
                 'AWAY_E_DEF_RATING', 'AWAY_DEF_RATING', 'AWAY_E_NET_RATING', 'AWAY_NET_RATING',
                 'HOME_PIE', 'AWAY_PIE', 'AWAY_E_USG_PCT', 'AWAY_E_TM_TOV_PCT', 'HOME_E_USG_PCT',
                 'HOME_E_TM_TOV_PCT'])
    
        
    # Calculate correlation matrix
    # corr = data.corr()

    # # Plot heatmap of correlation matrix
    # plt.figure(figsize=(12, 10))
    # sns.heatmap(corr, annot=True, cmap='coolwarm')
    # plt.show()
    y = y.map({'W': 1, 'L': 0})


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)

    # model.fit(X_train, y_train)

    # y_pred = model.predict(X_test)

    # accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)
    return model

def get_current_teams_data(home_team, away_team):
    # used to predict outcome

    home_id = teamID(home_team, teams)
    away_id = teamID(away_team, teams)
    
    home_team_stats = LeagueDashTeamStats(team_id_nullable=home_id, 
                                    measure_type_detailed_defense="Advanced", last_n_games=10).get_data_frames()[0]
    away_team_stats = LeagueDashTeamStats(team_id_nullable=away_id,
                                        measure_type_detailed_defense="Advanced", last_n_games=10).get_data_frames()[0]
    
    # used to predict outcome
    # rename HOME_AST_TO to HOME_AST_TOV
    home_team_stats.rename(columns={'AST_TO': 'AST_TOV'}, inplace=True)
    home_team_stats = home_team_stats.drop(
        columns=['TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 
                    'OFF_RATING_RANK', 'DEF_RATING_RANK', 'NET_RATING_RANK', 'AST_PCT_RANK', 
                    'AST_TO_RANK', 'AST_RATIO_RANK', 'OREB_PCT_RANK', 'DREB_PCT_RANK', 
                    'REB_PCT_RANK', 'TM_TOV_PCT_RANK', 'EFG_PCT_RANK', 'TS_PCT_RANK', 
                    'PACE_RANK', 'PIE_RANK', 'W_PCT', 'MIN', 'OFF_RATING', 
                    'E_OFF_RATING', 'DEF_RATING', 'E_DEF_RATING', 'NET_RATING', 'E_NET_RATING', 'PIE'])
    
    away_team_stats.rename(columns={'AST_TO': 'AST_TOV'}, inplace=True)
    away_team_stats = away_team_stats.drop(
        columns=['TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 
                    'OFF_RATING_RANK', 'DEF_RATING_RANK', 'NET_RATING_RANK', 'AST_PCT_RANK', 
                    'AST_TO_RANK', 'AST_RATIO_RANK', 'OREB_PCT_RANK', 'DREB_PCT_RANK', 
                    'REB_PCT_RANK', 'TM_TOV_PCT_RANK', 'EFG_PCT_RANK', 'TS_PCT_RANK', 
                    'PACE_RANK', 'PIE_RANK', 'W_PCT', 'MIN', 'OFF_RATING', 
                    'E_OFF_RATING', 'DEF_RATING', 'E_DEF_RATING', 'NET_RATING', 'E_NET_RATING', 'PIE'])
    
    # Rename columns with 'home_' and 'away_' prefix
    home_team_stats.columns = 'HOME_' + home_team_stats.columns
    away_team_stats.columns = 'AWAY_' + away_team_stats.columns

    # Reset index before joining
    home_team_stats.reset_index(drop=True, inplace=True)
    away_team_stats.reset_index(drop=True, inplace=True)

    # Concatenate along the columns axis
    team_stats = pd.concat([home_team_stats, away_team_stats], axis=1)
    return team_stats
model = train(data)
def predict(home_team, away_team):
    team_stats = get_current_teams_data(home_team, away_team)
    prediction = model.predict(team_stats)
    return prediction

a=0

from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

def cluster_and_visualize(data, n_clusters, n_components=2):

    data = data.drop(
        columns=['HOME_WL', 'AWAY_WL','HOME_GAME_ID', 'AWAY_GAME_ID', 'HOME_TEAM_ID', 'AWAY_TEAM_ID', 
                 'HOME_TEAM_NAME', 'HOME_TEAM_ABBREVIATION', 'HOME_TEAM_CITY', 
                 'HOME_USG_PCT', 'HOME_MIN', 'HOME_HOME', 'AWAY_TEAM_NAME', 'AWAY_TEAM_ABBREVIATION', 
                 'AWAY_TEAM_CITY', 'AWAY_USG_PCT', 'AWAY_MIN', 'AWAY_HOME', 
                 'HOME_E_OFF_RATING', 'HOME_OFF_RATING', 'HOME_E_DEF_RATING', 'HOME_DEF_RATING',
                 'HOME_E_NET_RATING', 'HOME_NET_RATING', 'AWAY_E_OFF_RATING', 'AWAY_OFF_RATING',
                 'AWAY_E_DEF_RATING', 'AWAY_DEF_RATING', 'AWAY_E_NET_RATING', 'AWAY_NET_RATING',
                 'HOME_PIE', 'AWAY_PIE', 'AWAY_E_USG_PCT', 'AWAY_E_TM_TOV_PCT', 'HOME_E_USG_PCT',
                 'HOME_E_TM_TOV_PCT'])

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    # Perform tsne
    tsne = TSNE(n_components=n_components, random_state=42)
    data_pca = tsne.fit_transform(data)

    # Create a KMeans instance with n_clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    
    # Fit the model to the PCA-transformed data
    kmeans.fit(data_pca)
    
    # Get the cluster assignments for each data point
    labels = kmeans.labels_
    
    # Plot the PCA-transformed data colored by the cluster assignments
    plt.scatter(data_pca[:, 0], data_pca[:, 1], c=labels, cmap='viridis')
    
    # Plot the cluster centers
    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='red', s=300, alpha=0.5)
    
    plt.show()

cluster_and_visualize(data, 5, 3)
