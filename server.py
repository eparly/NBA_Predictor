from flask import Flask, render_template
import pandas as pd
import os
import sys
from basketball5_2 import montecarlo
from basketball5_3 import spreads, scores, DOFactors
from Predictor_db.NBA_Predictor.db_management import *
from nba_odds_api import set_odds
from Predictor_db.NBA_Predictor.game_results import gameResults, pullGames, yesterdayGameData, yesterdayGames
from Predictor_db.NBA_Predictor.record import records
from datetime import datetime, timedelta

this_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(this_dir, 'flask-server\bball5_3_model.py'))

app = Flask(__name__)
today = datetime.today()
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
schedule = pd.read_csv(os.path.join(__location__, 'NBA_Schedule_2023_24.csv'))


@app.route('/')
def home():
    d = today.strftime('%a, %b %d, %Y').replace(" 0", " ")

    todayGames = schedule.loc[schedule['Date'] == d]
    todayIndex = todayGames.index
    results = []
    games = []

    results2 = []
    games2 = []

    results3 = []
    games3 = []

    results4 = []
    games4 = []

    results5 = []
    games5 = []

    results6 = []
    games6 = []

    spread_list = []

    odds = []
    margins = []

    record1 = []
    record2 = []
    record3 = []
    record4 = []
    record5 = []
    record6 = []
    for i in todayIndex:
        game = get_predictions('games', i)[0]
        results.append((game[3], game[4]))
        games.append(game)

        game2 = get_predictions('scores', i)[0]
        results2.append((game2[3], game2[4]))
        games2.append(game2)

        game3 = get_predictions('factors', i)[0]
        results3.append((game3[3], game3[4]))
        games3.append(game3)

        game4 = get_predictions('montecarlohomefactors', i)[0]
        results4.append((game4[3], game4[4]))
        games4.append(game4)

        game5 = get_predictions('streak_multiplier', i)[0]
        results5.append((game5[3], game5[4]))
        games5.append(game5)

        game6 = get_predictions('streak_factor', i)[0]
        results6.append((game6[3], game6[4]))
        games6.append(game6)



        todayOdds = get_predictions('odds', i)[0]
        odds.append(todayOdds)

        spread = get_predictions('spreads', i)[0]
        spread_list.append((spread[1], spread[2], spread[4], todayOdds[1]))

    game_results = get_results()
    predictions1 = get_predictions('games', "all")
    predictions2 = get_predictions('scores', "all")
    predictions3 = get_predictions('factors', "all")
    predictions4 = get_predictions('montecarlohomefactors', 'all')
    predictions5 = get_predictions('streak_multiplier', "all")
    predictions6 = get_predictions('streak_factor', "all")

    correct1, total1 = records(predictions1, game_results)
    correct2, total2 = records(predictions2, game_results)
    correct3, total3 = records(predictions3, game_results)
    correct4, total4 = records(predictions4, game_results)
    correct5, total5 = records(predictions5, game_results)
    correct6, total6 = records(predictions6, game_results)

    record1.append((correct1, total1, round(correct1/total1, 4)))
    record2.append((correct2, total2, round(correct2/total2, 4)))
    record3.append((correct3, total3, round(correct3/total3, 4)))
    record4.append((correct4, total4, round(correct4/total4, 4)))
    record5.append((correct5, total5, round(correct5/total5, 4)))
    record6.append((correct6, total6, round(correct6/total6, 4)))


    games.sort(key=lambda x: abs(x[3]-x[4]), reverse=True)
    games2.sort(key=lambda x: abs(x[3]-x[4]), reverse=True)
    games3.sort(key=lambda x: abs(x[3]-x[4]), reverse=True)
    games4.sort(key=lambda x: abs(x[3]-x[4]), reverse=True)
    games5.sort(key=lambda x: abs(x[3]-x[4]), reverse=True)
    games6.sort(key=lambda x: abs(x[3]-x[4]), reverse=True)


    spread_list.sort(key=lambda x: abs(x[3]) - abs(x[2]), reverse=True)

    while (len(games) < 6*5):
        games.append((0, 'no game', 'no game', 0, 0, 0))
        games2.append((0, 'no game', 'no game', 0, 0, 0))
        games3.append((0, 'no game', 'no game', 0, 0, 0))
        games4.append((0, 'no game', 'no game', 0, 0, 0))
        games5.append((0, 'no game', 'no game', 0, 0, 0))
        games6.append((0, 'no game', 'no game', 0, 0, 0))

    winners = [row[0] for row in spread_list]
    spread = [row[1] for row in spread_list]
    return render_template("template1.html", model1=games, model2=games2, model3=games3, model4=games4, model5=games5, model6=games6,
                           home=winners, spread=spread_list, model_1=record1, model_2=record2, 
                           model_3=record3, model_4=record4, model_5=record5, model_6=record6, 
                           odds=odds)


@ app.route('/game_id/<game_id>')
def game_id(game_id):
    values = get_predictions('games', game_id)
    results = {
        "results": "Predicted",
        "gameID": game_id,
        "hometeam": values[0][1],
        "homescore": values[0][3],
        "awayteam": values[0][2],
        "awayscore": values[0][4]
    }
    return results


@ app.route('/record')
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
    return score


@ app.route('/results')
def results():
    values = 'No game played yesterday'
    gameIds= yesterdayGames(yesterday)
    first = min(gameIds)
    last = max(gameIds)
    while first <= last:
        game = pullGames(first)
        values = gameResults(game)
        insert_results(values)
        first = '%010d' % (int(first)+1)

    return values


@ app.route('/update')
def update_results():
    values = 'no games'
    start_id = '0022200001'
    print('starting')
    gameIds = yesterdayGames(yesterday)
    first = min(gameIds)
    last = max(gameIds)
    print(last)
    while start_id != last:
        game = pullGames(start_id)
        values = gameResults(game)
        insert_results(values)
        start_id = '%010d' % (int(start_id)+1)
        print(start_id)
    return values


@app.route("/odds")
def odds():
    d = today.strftime('%a, %b %d, %Y').replace(" 0", " ")
    todayGames = schedule.loc[schedule['Date'] == d]
    todayIndex = list(todayGames.index)

    odds = get_predictions('odds', list(todayIndex)[-1])
    if odds == [(0, 0, 0, 0, 0, 0)]:
        todayOdds = set_odds(todayIndex)
        return todayOdds
    else:
        return odds


@ app.route("/games")
def predictions():

    # look into async functions to create threads

    d = today.strftime('%a, %b %d, %Y').replace(" 0", " ")
    i = 1
    n = 0

    results = []
    todayGames = schedule.loc[schedule['Date'] == d]
    todayIndex = todayGames.index

    predictions = get_predictions('games', list(todayIndex)[-1])
    if (predictions == [(0, 0, 0, 0, 0, 0)]):

        values = 'No game today'
        for i in todayIndex:
            hometeam = schedule.at[i, "Home/Neutral"]
            awayteam = schedule.at[i, "Visitor/Neutral"]

            values = montecarlo(i, hometeam, awayteam)
            insert_predictions(values)

            spread = spreads(i, hometeam, awayteam)
            insert_spreads(spread)

            score = scores(i, hometeam, awayteam)
            insert_scores(score)

            factors = DOFactors(i, hometeam, awayteam)
            insert_factors(factors)

            results.append(factors)
        return results
    else:
        return predictions


if __name__ == "__main__":
    app.run(debug=True)
