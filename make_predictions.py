from datetime import datetime, timedelta
from Predictor_db.NBA_Predictor.record import records
from Predictor_db.NBA_Predictor.db_management import *
from basketball5_3 import spreads, scores, DOFactors, homeFactors
from basketball5_2 import montecarlo, teamID
from streak_multiplier import streakMultiplier
from historic_data.advanced_data import predict
import time as t
import pandas as pd
import pickle
import json
import os

today = datetime.today()
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
schedule = pd.read_csv(os.path.join(__location__, 'NBA_Schedule_2023_24.csv'))
with open(os.path.join(__location__, 'streak_data'), 'rb') as file:
    team_results = pickle.load(file)

with open(os.path.join(__location__, 'streak_point_changes'), 'rb') as file:
    streak_point_changes = pickle.load(file)


def predictions():

    # look into async functions to create threads

    d = today.strftime('%a, %b %d, %Y').replace(" 0", " ")
    # d = (datetime.now() - timedelta(1)).strftime('%a, %b %d, %Y').replace(" 0", " ")
    i = 1
    n = 0

    results = []
    todayGames = schedule.loc[schedule['Date'] == d]
    todayIndex = list(todayGames.index)

    k = 0
    while True:
        try:
            values = 'No game today'
            k = 0
            for i in todayIndex:
                prediction = get_predictions(
                    'home_streak_multiplier', list(todayIndex)[k])
                if prediction == [(0, 0, 0, 0, 0, 0, 0)]:
                    hometeam = schedule.at[i, "Home/Neutral"]
                    awayteam = schedule.at[i, "Visitor/Neutral"]
                    # prediction = predict(hometeam, awayteam)
                    home_multiplier = streakMultiplier(hometeam)
                    t.sleep(3)

                    away_multiplier = streakMultiplier(awayteam)
                    t.sleep(3)
                    game_multiplier = [home_multiplier, away_multiplier]

                    values = montecarlo(i, hometeam, awayteam)
                    if values == []:
                        continue
                    insert_predictions(values, 'games', today)

                    homeFactor = montecarlo(
                        i, hometeam, awayteam, homeFactor=True)
                    insert_predictions(
                        homeFactor, 'montecarlohomefactors', today)

                    homeFactor = homeFactors(i, hometeam, awayteam)
                    insert_spreads(homeFactor, 'homefactor_spreads', today)

                    spread = spreads(i, hometeam, awayteam)
                    insert_spreads(spread, 'spreads', today)

                    score = scores(i, hometeam, awayteam)
                    insert_scores(score, today)

                    factors = DOFactors(i, hometeam, awayteam)
                    insert_factors(factors, today)

                    streaks_multipliers = montecarlo(
                        i, hometeam, awayteam, multiplier=game_multiplier, streak_mode='multiplier')
                    insert_predictions(streaks_multipliers,
                                       'streak_multiplier', today)

                    streaks_factors = montecarlo(
                        i, hometeam, awayteam, multiplier=game_multiplier, streak_mode='factor')
                    insert_predictions(streaks_factors, 'streak_factor', today)

                    home_streak_multiplier = montecarlo(
                        i, hometeam, awayteam, multiplier=game_multiplier, streak_mode='multiplier', homeFactor=True)
                    insert_predictions(home_streak_multiplier,
                                       'home_streak_multiplier', today)

                    results.append(home_streak_multiplier)
                k += 1

            return results
        except json.decoder.JSONDecodeError:
            continue
