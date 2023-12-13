# from db_management import *


from datetime import datetime

from spreads import spread_results
from Predictor_db.NBA_Predictor.db_management import get_predictions, get_results, insert_record


def update_records(): 
    today = datetime.today()

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

    score = spread_results('home_spread_picks')
    insert_record(today, score, 'home_spread_picks_record')
    
    scores = get_predictions('home_streak_multiplier', 'all')
    correct, games = records(scores, results)

    score = {
        "correct": correct,
        "total": games,
        "percentage": round(correct/games, 4)
    }
    insert_record(today, score, 'home_streak_multiplier_record')
    return score

def records(predictions, results):
    games = 0
    correct = 0

    game_ids = [x[0] for x in predictions]
    for i in game_ids:
        prediction = [x for x in predictions if x[0] == i]
        result = [x for x in results if int(x[0])== i]

        if (prediction and result):
            prediction = prediction[0]
            result = result[0]
            games += 1
            if ((prediction[3]-prediction[4]) >= 0 and (result[3]-result[4]) >= 0):
                correct += 1

            if ((prediction[3]-prediction[4]) <= 0 and (result[3]-result[4]) <= 0):
                correct += 1
    return correct, games
