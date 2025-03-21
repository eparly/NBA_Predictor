import os
import joblib
from nba_api_service.get_stats import get_data 
from Predictor_db.NBA_Predictor.db_management import get_results
import pandas as pd
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
schedule = pd.read_csv('src/schedules/NBA_Schedule_2023_24.csv')

predictions = []


def spreads(i, hometeam, awayteam):
    reg = joblib.load('basketball5_3.joblib')

    values = get_data(hometeam, awayteam, 0.5)
    values = values[['fgp_a', 'fg3_a', 'ftp_a', 'reb_a', 'stl_a', 'blk_a', 'tov_a',
                    'fgp_b', 'fg3_b', 'ftp_b', 'reb_b', 'stl_b', 'blk_b', 'tov_b']]
    prediction = reg.predict(values)
    return i, prediction[0][0], prediction[0][1], hometeam, awayteam


def scores(i, hometeam, awayteam):
    reg = joblib.load(os.path.join(__location__, 'basketball5_3_score.joblib'))
    values = get_data(hometeam, awayteam, 0.5)
    values = values[['fgp_a', 'fg3_a', 'ftp_a', 'reb_a', 'stl_a', 'blk_a', 'tov_a',
                    'fgp_b', 'fg3_b', 'ftp_b', 'reb_b', 'stl_b', 'blk_b', 'tov_b']]
    prediction = reg.predict(values)
    return i, prediction[0][0], prediction[0][1], hometeam, awayteam


def DOFactors(i, hometeam, awayteam):
    reg = joblib.load(os.path.join(__location__, "basketball5_3_DOFactors.joblib"))
    values = get_data(hometeam, awayteam, 0.3)
    values = values[['fgp_a', 'fg3_a', 'ftp_a', 'reb_a', 'stl_a', 'blk_a', 'tov_a',
                    'fgp_b', 'fg3_b', 'ftp_b', 'reb_b', 'stl_b', 'blk_b', 'tov_b']]
    prediction = reg.predict(values)
    return i, prediction[0][0], prediction[0][1], hometeam, awayteam


def Normalized(i, hometeam, awayteam):
    reg = joblib.load(os.path.join(__location__, "basketball5_3_Normalized.joblib"))
    values = get_data(hometeam, awayteam, 0.3)
    values = values[['fgp_a', 'fg3_a', 'ftp_a', 'reb_a', 'stl_a', 'blk_a', 'tov_a',
                    'fgp_b', 'fg3_b', 'ftp_b', 'reb_b', 'stl_b', 'blk_b', 'tov_b']]
    prediction = reg.predict(values)

    return i, prediction[0][0], prediction[0][1], hometeam, awayteam


def homeFactors(i, hometeam, awayteam):
    reg = joblib.load(os.path.join(__location__, "basketball5_3_HomeFactors.joblib"))
    values = get_data(hometeam, awayteam, 0.5)
    prediction = reg.predict(values)

    return i, prediction[0][0], prediction[0][0], hometeam, awayteam

# homeFactors(70, 'Memphis Grizzlies', 'San Antonio Spurs')
# Normalized(0, 'Memphis Grizzlies', 'San Antonio Spurs')


# for i in range(10):
#     values = get_data(schedule.at[i, "Home/Neutral"],
#                       schedule.at[i, "Visitor/Neutral"])

#     prediction = reg.predict(values)
#     result = [prediction, schedule.at[i, "Home/Neutral"],
#               schedule.at[i, "Visitor/Neutral"]]
#     predictions.append(result)

# results = get_results()
# spread_score = []
# for i in range(len(predictions)):
#     actual_spread = abs(results[i][3] - results[i][4])
#     predicted_spread = abs(predictions[i][0][0][0])

#     spread_score.append(abs(actual_spread-predicted_spread))
