from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize, Normalizer
import numpy as np
import pandas as pd
import joblib

from Predictor_db.NBA_Predictor.db_management import get_historic
# from Predictor_db.NBA_Predictor.historic_data import set_historic


def group_games(games):

    games = games.sort_values(by=['game_id'])
    games1 = games.drop_duplicates(subset=['game_id'], keep='first')
    games2 = games.drop_duplicates(subset=['game_id'], keep='last')
    games = games1.merge(games2, on='game_id')

    return games


games = get_historic()
games = pd.DataFrame(games, columns=["game_id", "PTS", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM",
                     "FTA", "FT_PCT", "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV", "PF", "PLUS_MINUS", "WL", "HOME"])


games = group_games(games)

spreads = games[["PLUS_MINUS_x"]].copy()
data = games[['FG_PCT_x', 'FGA_x', 'FG3_PCT_x', 'FT_PCT_x', 'REB_x', 'STL_x', 'BLK_x', 'TOV_x', 'HOME_x',
              'FG_PCT_y', 'FGA_y', 'FG3_PCT_y', 'FT_PCT_y', 'REB_y', 'STL_y', 'BLK_y', 'TOV_y', 'HOME_y']].copy()


X_train, X_test, y_train, y_test = train_test_split(
    data, spreads, test_size=0.3)

reg = MultiOutputRegressor(RandomForestRegressor(
    n_estimators=1000)).fit(X_train, y_train)

joblib.dump(reg, './flask-server/basketball5_3_HomeFactors')

print(reg.score(X_test, y_test))
