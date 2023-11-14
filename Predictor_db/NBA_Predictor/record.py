# from db_management import *


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
