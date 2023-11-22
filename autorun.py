import os
import json
import pickle
import pandas as pd
import time as t
from nba_api.stats.static import teams

from basketball5_2 import montecarlo, teamID
from basketball5_3 import spreads, scores, DOFactors, homeFactors
from Predictor_db.NBA_Predictor.db_management import *
from spreads import spread_picks, spread_results
from streaks import get_streak
from nba_odds_api import set_odds
from Predictor_db.NBA_Predictor.game_results import gameResults, pullGames, yesterdayGames, matchGameIds
from Predictor_db.NBA_Predictor.record import records
from datetime import datetime, timedelta

today = datetime.today()
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
schedule = pd.read_csv(os.path.join(__location__, 'NBA_Schedule_2023_24.csv'))
with open(os.path.join(__location__, 'streak_data'), 'rb') as file:
    team_results = pickle.load(file)

with open(os.path.join(__location__, 'streak_point_changes'), 'rb') as file:
    streak_point_changes = pickle.load(file)

def teamName(teamname, teams):

    teams = teams.get_teams()
    ID = [x for x in teams if x['full_name'] == teamname][0]
    ID = ID['abbreviation']
    return ID

def streakMultiplier(teamname):
    streak_info = get_streak(teamName(teamname, teams)).split(' ')
    if streak_info == ['']:
        return 1
    streak_type = streak_info[0]
    streak_length = int(streak_info[1])
    streak_data = streak_point_changes
    if (streak_length == 1):
        return 1
    streak_multiplier = streak_data[streak_type, streak_length]
    return streak_multiplier

def predictions():

    # look into async functions to create threads

    d = today.strftime('%a, %b %d, %Y').replace(" 0", " ")
    i = 1
    n = 0

    results = []
    todayGames = schedule.loc[schedule['Date'] == d]
    todayIndex = list(todayGames.index)

    k=0
    while True:
        try:
            values = 'No game today'
            k=0
            for i in todayIndex:
                prediction = get_predictions('home_streak_multiplier', list(todayIndex)[k])
                prediction = [(0, 0, 0, 0, 0, 0, 0)]
                if prediction == [(0, 0, 0, 0, 0, 0, 0)]:
                    hometeam = schedule.at[i, "Home/Neutral"]
                    awayteam = schedule.at[i, "Visitor/Neutral"]
                    
                    home_multiplier = streakMultiplier(hometeam)
                    t.sleep(3)
                    
                    away_multiplier = streakMultiplier(awayteam)
                    t.sleep(3)
                    game_multiplier = [home_multiplier,away_multiplier]

                    values = montecarlo(i, hometeam, awayteam)
                    if values == []:
                        continue
                    insert_predictions(values, 'games', today)

                    homeFactor = montecarlo(i, hometeam, awayteam, homeFactor=True)
                    insert_predictions(homeFactor, 'montecarlohomefactors', today)

                    homeFactor = homeFactors(i, hometeam, awayteam)
                    insert_spreads(homeFactor, 'homefactor_spreads', today)

                    spread = spreads(i, hometeam, awayteam)
                    insert_spreads(spread, 'spreads', today)

                    score = scores(i, hometeam, awayteam)
                    insert_scores(score, today)

                    factors = DOFactors(i, hometeam, awayteam)
                    insert_factors(factors, today)

                    streaks_multipliers = montecarlo(i, hometeam, awayteam, multiplier=game_multiplier, streak_mode='multiplier')
                    insert_predictions(streaks_multipliers, 'streak_multiplier', today)

                    streaks_factors = montecarlo(i, hometeam, awayteam, multiplier=game_multiplier, streak_mode='factor')
                    insert_predictions(streaks_factors, 'streak_factor', today)

                    home_streak_multiplier = montecarlo(i, hometeam, awayteam, multiplier=game_multiplier, streak_mode='multiplier', homeFactor=True)
                    insert_predictions(home_streak_multiplier, 'home_streak_multiplier', today)

                    results.append(home_streak_multiplier)
                k+=1

            
            return results
        except json.decoder.JSONDecodeError:
            continue


def record():
    correct = 0
    games = 0
    games_2 = 0
    results = get_results()
    predictions = get_predictions('games', "all")
    correct, games = records(predictions, results)
    if games == 0:
        return
    score = {
        "correct": correct,
        "total": games,
        "percentage": round(correct/games, 4)
    }
    insert_record(today, score, 'record')

    scores = get_predictions('scores', 'all')
    correct, games = records(scores, results)

    score = {
        "correct": correct,
        "total": games,
        "percentage": round(correct/games, 4)
    }
    insert_record(today, score, 'record_2')

    scores = get_predictions('factors', 'all')
    correct, games = records(scores, results)

    score = {
        "correct": correct,
        "total": games,
        "percentage": round(correct/games, 4)
    }
    insert_record(today, score, 'record_3')

    scores = get_predictions('montecarlohomefactors', 'all')
    correct, games = records(scores, results)

    score = {
        "correct": correct,
        "total": games,
        "percentage": round(correct/games, 4)
    }
    insert_record(today, score, 'record_4')

    scores = get_predictions('streak_multiplier', 'all')
    correct, games = records(scores, results)

    score = {
        "correct": correct,
        "total": games,
        "percentage": round(correct/games, 4)
    }
    insert_record(today, score, 'streak_multiplier_record')

    scores = get_predictions('streak_factor', 'all')
    correct, games = records(scores, results)

    score = {
        "correct": correct,
        "total": games,
        "percentage": round(correct/games, 4)
    }
    insert_record(today, score, 'streak_factor_record')

    score = spread_results('spread_picks')
    insert_record(today, score, 'spread_picks_record')
    return score


def results():
    values = 'No game played yesterday'
    gameData = matchGameIds()
    for game in gameData:
        values = gameResults(game)
        insert_results(values, today)
    # gameIds = yesterdayGames(yesterday)
    # if len(gameIds)==0:
    #     return values
    # for i in gameIds:
    #     game = pullGames(i)
    #     values = gameResults(game)
    #     insert_results(values, today)

    return values


def odds():
    d = today.strftime('%a, %b %d, %Y').replace(" 0", " ")
    todayGames = schedule.loc[schedule['Date'] == d]
    todayIndex = list(todayGames.index)
    if todayIndex == []:
        return

    odds = get_predictions('odds', list(todayIndex)[-1])
    if odds == [(0, 0, 0, 0, 0, 0, 0)]:
        todayOdds = set_odds()
        return todayOdds
    else:
        return odds


results()
record()
predictions()
odds()
spread_picks('spreads')
spread_picks('homefactor_spreads')

