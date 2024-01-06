from calculate_net_units import update_units
from Predictor_db.NBA_Predictor.game_results import results
from odds import odds
from Predictor_db.NBA_Predictor.record import update_records
from spreads import spread_picks
from make_predictions import predictions

results()
update_records()
update_units()
predictions()
odds()
spread_picks('spreads')
spread_picks('homefactor_spreads')

# TODO
# 1. Add db table for advanced picks