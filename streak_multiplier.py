import os
import pickle
from streaks import get_streak
from team_name import teamName
from nba_api.stats.static import teams



def streakMultiplier(teamname):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'streak_point_changes'), 'rb') as file:
        streak_point_changes = pickle.load(file)
    streak_info = get_streak(teamName(teamname, teams)).split(' ')
    streak_type = streak_info[0]
    streak_length = int(streak_info[1])
    streak_data = streak_point_changes
    if (streak_length == 1):
        return 1
    streak_multiplier = streak_data[streak_type, streak_length]
    return streak_multiplier
