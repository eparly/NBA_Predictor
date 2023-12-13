import requests
import numpy as np
import json
import unittest.mock

from Predictor_db.NBA_Predictor.db_management import insert_spread_odds, insert_ml_odds, get_predictions
from mock_odds_response import mock_odds_response
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get('API_KEY')

def match_order(odds_data, predictions):
    odds_data = np.array(odds_data)
    predictions = np.array(predictions)

    game_order = []
    for j in range(len(odds_data)):
        game_id = [i for i in range(len(
            predictions)) if odds_data[:, 1:3][j][0] == predictions[:, 1:3][i][0] and odds_data[:, 1:3][j][1] == predictions[:, 1:3][i][1]]
        if len(game_id) == 0:
            break
        game_id = predictions[game_id[-1]][0]

        game_order.append(game_id)

    return game_order


def set_odds():
    predictions = get_predictions('games', 'all')

    url = "https://sportspage-feeds.p.rapidapi.com/games"
    querystring = {"league": "NBA"}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "sportspage-feeds.p.rapidapi.com"
    }

    if predictions == ([0, 0, 0, 0, 0, 0]):
        response = unittest.mock.MagicMock()
        response.json.return_value = mock_odds_response
    else:
        response = requests.get(url, headers=headers, params=querystring)
        a=0

    games = len(response.json()['results'])

    # games from this api arent in the same order as the other one, need to enter these ones in the same order as we do for all predictions
    odds_data = []
    ml_data = []
    i = 0
    for i in range(games):
        if "odds" not in response.json()['results'][i]:
            return 'no odds yet, check back later'
        spreads = response.json(
        )['results'][i]['odds'][0]['spread']['current']['home']
        moneyline_home = response.json(
        )['results'][i]['odds'][0]['moneyline']['current']['homeOdds']
        moneyline_home = american_to_decimal(moneyline_home)
        moneyline_away = response.json(
        )['results'][i]['odds'][0]['moneyline']['current']['awayOdds']
        moneyline_away = american_to_decimal(moneyline_away)
        hometeam = response.json()['results'][i]['teams']['home']['team']
        awayteam = response.json()['results'][i]['teams']['away']['team']

        odds_data.append((spreads, hometeam, awayteam))
        ml_data.append((moneyline_home, moneyline_away, hometeam, awayteam))
    matched_order = match_order(odds_data, predictions)

    ordered_odds = []
    ordered_ml = []
    for i in range(len(matched_order)):
        ordered_odds.append((
            matched_order[i], odds_data[i][0], odds_data[i][1], odds_data[i][2]))
        ordered_ml.append((
            matched_order[i], ml_data[i][0], ml_data[i][1], ml_data[i][2], ml_data[i][3]))
        insert_spread_odds(values=ordered_odds[i])
        insert_ml_odds(values=ordered_ml[i])

    return odds_data


def american_to_decimal(american_odds):
    if american_odds < 0:
        decimal_odds = -100 / american_odds + 1
    else:
        decimal_odds = american_odds / 100 + 1

    return round(decimal_odds, 2)
# game_ids = [
#     427,
#     428,
#     429,
#     430,
#     431,
#     432,
#     433,
#     434,
#     435,
#     436
# ]
# predictions = get_predictions('games', 'all')
# set_odds()
# odds = get_predictions('odds', 'all')
# match_order(odds, predictions)

# set_odds()
