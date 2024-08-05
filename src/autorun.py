from odds.odds import odds
from predictions.spreads import spread_picks
from predictions.make_predictions import predictions


predictions()
odds()
spread_picks('spreads')
spread_picks('homefactor_spreads')

# TODO
# 1. Get pace data using measure type: advanced, use that to calculate number of possessions
# 2. Create ML model for spreads using advanced data. Need to get historical data first, try querying the boxscores endpoint