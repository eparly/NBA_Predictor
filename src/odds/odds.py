from datetime import datetime
import os
from odds.nba_odds_api import set_odds

import pandas as pd

from Predictor_db.NBA_Predictor.db_management import get_predictions


def odds():
    today = datetime.today()
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    schedule = pd.read_csv(os.path.join(
        __location__, 'NBA_Schedule_2023_24.csv'))

    d = today.strftime('%a, %b %d, %Y').replace(" 0", " ")
    todayGames = schedule.loc[schedule['Date'] == d]
    todayIndex = list(todayGames.index)
    if todayIndex == []:
        return

    odds = get_predictions('ml_odds', list(todayIndex)[-1])
    if odds == [(0, 0, 0, 0, 0, 0, 0)]:
        todayOdds = set_odds()
        return todayOdds
    else:
        return odds
