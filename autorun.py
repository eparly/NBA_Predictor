from Predictor_db.NBA_Predictor.game_results import results
from odds import odds
from Predictor_db.NBA_Predictor.record import update_records
from spreads import spread_picks
from make_predictions import predictions

results()
update_records()
predictions()
odds()
spread_picks('spreads')
spread_picks('homefactor_spreads')

# TODO
# 1. DONE ---- record ml odds, convert from american to decimal - new table 
# 2. record ml picks for each model - new table for each model
# 3. track the record of each model in terms of units gained/lost over time - new table for each model
# 4. Far future: create a betting plan based on expected value of each bet, 
# coming from the model's confidence in its prediction, and a daily budget in units