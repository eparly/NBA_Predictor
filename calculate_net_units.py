from datetime import datetime
from Predictor_db.NBA_Predictor.db_management import get_predictions, get_results, get_ml_odds, insert_units
from utils import get_winner

def calculate_units(table):
    predictions = get_predictions(table, 'all')
    results = get_results()
    ml_odds = get_ml_odds()
    odds_game_ids = [x[0] for x in ml_odds]
    prediction_game_ids = [x[0] for x in predictions]
    game_ids_with_odds = [x for x in prediction_game_ids if x in odds_game_ids]
    units_won = 0
    for i in game_ids_with_odds:
        prediction = [x for x in predictions if x[0] == i][0]
        result = [x for x in results if int(x[0]) == i][0]
        odds = [x for x in ml_odds if int(x[0]) == i][0]
        predicted_winner = get_winner(prediction)
        actual_winner = get_winner(result)
        if predicted_winner == actual_winner:
            if predicted_winner == 'home':
                units_won += odds[1]
            else:
                units_won += odds[2]
    units_won -= len(game_ids_with_odds)
    return units_won


def update_units():
    today = datetime.today()

    games_units = calculate_units('games')
    scores_units = calculate_units('scores')
    factors_units = calculate_units('factors')
    montecarlohomefactors_units = calculate_units('montecarlohomefactors')
    streak_multiplier_units = calculate_units('streak_multiplier')
    streak_factor_units = calculate_units('streak_factor')
    home_streak_multiplier_units = calculate_units('home_streak_multiplier')

    units = {
        "games": games_units,
        "scores": scores_units,
        "factors": factors_units,
        "montecarlohomefactors": montecarlohomefactors_units,
        "streak_multiplier": streak_multiplier_units,
        "streak_factor": streak_factor_units,
        "home_streak_multiplier": home_streak_multiplier_units
    }
    insert_units(today, units, 'units')

# calculate_units('games')
