import json
import pandas as pd

from basketball5_2 import montecarlo
from basketball5_3 import spreads, scores, DOFactors, homeFactors
from Predictor_db.NBA_Predictor.db_management import *
from spreads import spread_picks
from nba_odds_api import set_odds
from Predictor_db.NBA_Predictor.game_results import gameResults, pullGames, firstLast
from Predictor_db.NBA_Predictor.record import records
from datetime import datetime, timedelta

today = datetime.today()
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
schedule = pd.read_excel('flask-server/NBA_2023_schedule.xlsx')


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
                prediction = get_predictions('factors', list(todayIndex)[k])
                if prediction == [(0, 0, 0, 0, 0, 0, 0)]:
                    hometeam = schedule.at[i, "Home/Neutral"]
                    awayteam = schedule.at[i, "Visitor/Neutral"]

                    values = montecarlo(i, hometeam, awayteam)
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

                    results.append(factors)
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
    return score


def results():
    values = 'No game played yesterday'
    first, last = firstLast(yesterday)
    if first == '':
        return values
    while first <= last:
        game = pullGames(first)
        values = gameResults(game)
        insert_results(values, today)
        first = '%010d' % (int(first)+1)

    return values


def odds():
    d = today.strftime('%a, %b %d, %Y').replace(" 0", " ")
    todayGames = schedule.loc[schedule['Date'] == d]
    todayIndex = list(todayGames.index)

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
