from Predictor_db.NBA_Predictor.db_management import get_predictions, insert_spread_picks, get_results
from Predictor_db.NBA_Predictor.game_results import gameResults, yesterdayGameData




def spread_picks(table, gameResults = False, spreads = []):
    if spreads == []:
        spreads = get_predictions(table, 'all')

    odds = get_predictions('odds', 'all')

    odds_dict = {odd[0]: odd for odd in odds}
    combined = []
    picks = []
    for spread in spreads:
        if spread[0] in odds_dict:
            combined_tuple = spread[:3] + \
                spread[4:5] + (odds_dict[spread[0]][1:2])

            combined.append(combined_tuple)

            if abs(combined_tuple[3]) >= abs(combined_tuple[4]):
                if combined_tuple[3] > 0 and combined_tuple[4] > 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[2], -1*combined_tuple[4]))
                if combined_tuple[3] < 0 and combined_tuple[4] < 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[1], combined_tuple[4]))

                if combined_tuple[3] > 0 and combined_tuple[4] < 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[2], -1*combined_tuple[4]))
                if combined_tuple[3] < 0 and combined_tuple[4] > 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[1], combined_tuple[4]))
            else:
                if combined_tuple[3] > 0 and combined_tuple[4] > 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[1], combined_tuple[4]))
                if combined_tuple[3] < 0 and combined_tuple[4] < 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[2], -1*combined_tuple[4]))

                if combined_tuple[3] > 0 and combined_tuple[4] < 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[2], -1*combined_tuple[4]))
                if combined_tuple[3] < 0 and combined_tuple[4] > 0:
                    picks.append(
                        (combined_tuple[0], combined_tuple[1], combined_tuple[4]))
    if gameResults:
        return picks
    if table == 'spreads':
        insert_table = 'spread_picks'
    if table == 'homefactor_spreads':
        insert_table = 'home_spread_picks'
    for i in range(len(picks)):
        insert_spread_picks(picks[i], insert_table)
    a = 0


def spread_results(table):
    results = get_results()

    actualSpreads = []
    games = []
    for game in results:
        gameList = list(game)
        actualSpread = game[3] - game[4]
        gameList[3] = actualSpread
        gameList[4] = actualSpread * -1
        games.append(tuple(gameList))
        a=0
    spreads = get_predictions(table, "all")

  
    winningPicks = spread_picks('spreads', True, games)
    correct = 0

    j=0
    for i in range(len(spreads)):
        for j in range(len(winningPicks)):
            if spreads[i][0] == winningPicks[j][0]:
                if spreads[i][1] == winningPicks[j][1]:
                    if spreads[i][2] == winningPicks[j][2]:
                        correct+=1

    score = {
        "correct": correct,
        "total": len(winningPicks),
        "percentage": round(correct/len(winningPicks), 4)
    }

    return score
    


    a=0

spread_results('spread_picks')