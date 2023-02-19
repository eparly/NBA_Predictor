# import team data
from collections import Counter
import math
from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguedashptteamdefend
import random as r
import time


from datetime import datetime


today = datetime.today()
# schedule=pd.read_excel(r'C:\Users\13432\Documents\NBA_Schedule.xlsx')

d = today.strftime("%a, %b %d, %Y")


t = time
c = 0
n = 0
over = 0
under = 0
N = 15


def teamID(teamname, teams):

    teams = teams.get_teams()
    ID = [x for x in teams if x['full_name'] == teamname][0]
    ID = ID['id']
    return ID
# calculate 2 pointers on average
# gathering team stats


def offense_stats(teamname, location):

    teamstat = leaguedashteamstats.LeagueDashTeamStats(
        team_id_nullable=teamID(teamname, teams), last_n_games=N, location_nullable=location, per_mode_detailed="PerGame").get_data_frames()[0]
    if (len(teamstat)==0):
        teamstat = leaguedashteamstats.LeagueDashTeamStats(
            team_id_nullable=teamID(teamname, teams), per_mode_detailed="PerGame").get_data_frames()[0]
    return teamstat


def defense_stats(teamname, location):
    teamstat = leaguedashptteamdefend.LeagueDashPtTeamDefend(team_id_nullable=teamID(
        teamname, teams), last_n_games_nullable=N, location_nullable=location, per_mode_simple="PerGame").get_data_frames()[0]
    return teamstat


def defense_3stats(teamname, location):
    try:
        teamstat = leaguedashptteamdefend.LeagueDashPtTeamDefend(defense_category='3 Pointers', team_id_nullable=teamID(
            teamname, teams), last_n_games_nullable=N, location_nullable=location, per_mode_simple="PerGame").get_data_frames()[0]
    except:
        teamstat = leaguedashptteamdefend.LeagueDashPtTeamDefend(defense_category='3 Pointers', team_id_nullable=teamID(
            teamname, teams), per_mode_simple="PerGame").get_data_frames()[0]
    return teamstat


def montecarlo(gameID, hometeam, awayteam, homeFactor=False):
    home = ''
    away = ''
    global N
    N = 15
    if homeFactor:
        home = 'Home'
        away = 'Road'
        N = 30

    O_H = offense_stats(hometeam, home)
    D_H = defense_stats(hometeam, home)
    D3_H = defense_3stats(hometeam, home)

    O_A = offense_stats(awayteam, away)
    D_A = defense_stats(awayteam, away)
    D3_A = defense_3stats(awayteam, away)
    # calculating 2 pointers home
    fga_a = (O_H['FGA']-O_H['FG3A']+D_A['D_FGA']-D3_A['FG3A'])/2
    fgp_a = (O_H['FG_PCT']+D_A['D_FG_PCT'])/2

    # claculating 3 pointers made home
    tfga_a = (O_H['FG3A']+D3_A['FG3A'])/2
    tfgp_a = (O_H['FG3_PCT']+D3_A['FG3_PCT'])/2

    # calculating ftm home
    fta_a = O_H['FTA']
    ft_p_a = O_H['FT_PCT']

    # calculating 2 pointers away
    fga_b = (O_A['FGA']-O_A['FG3A']+D_H['D_FGA']-D3_H['FG3A'])/2
    fgp_b = (O_A['FG_PCT']+D_H['D_FG_PCT'])/2

    # claculating 3 pointers made away
    tfga_b = (O_A['FG3A']+D3_H['FG3A'])/2
    tfgp_b = (O_A['FG3_PCT']+D3_H['FG3_PCT'])/2

    # calculating ftm away
    fta_b = O_A['FTA']
    ft_p_b = O_A['FT_PCT']

    c = 0
    d = 0

    games = 1000
    homescore = 0
    awayscore = 0
    pointsA = 0
    pointsB = 0
    d = 0

    spread = []
    for j in range(games):
        pointsA = 0
        pointsB = 0
        # simulating 2 point shots
        if math.isnan(fga_a[0]):
            break
        for i in range(int(fga_a[0])):
            n = r.random()
            if n < fgp_a[0]:
                pointsA += 2
        # simulating 3 point shots
        for i in range(int(tfga_a[0])):
            n = r.random()
            if n < tfgp_a[0]:
                pointsA += 3
              # simulating free throws
        for i in range(int(fta_a[0])):
            n = r.random()
            if n < ft_p_a[0]:
                pointsA += 1

        # simulating 2 point shots
        for i in range(int(fga_b[0])):
            n = r.random()
            if n < fgp_b[0]:
                pointsB += 2
        # simulating 3 point shots
        for i in range(int(tfga_b[0])):
            n = r.random()
            if n < tfgp_b[0]:
                pointsB += 3
              # simulating free throws
        for i in range(int(fta_b[0])):
            n = r.random()
            if n < ft_p_b[0]:
                pointsB += 1

        homescore += pointsA
        awayscore += pointsB
        spread.append(pointsA-pointsB)
        if pointsA > pointsB:
            c += 1
        if pointsB > pointsA:
            d += 1

    if c > d:
        confidence = c/(games)
    if d > c:
        confidence = d/(games)
    if c == d:
        confidence = 0.5

    homescore = homescore/(games)
    awayscore = awayscore/(games)

    # results
    spreads = Counter(sorted(spread))
    k = list(spreads.keys())
    v = list(spreads.values())
    values = {
        "gameID": gameID,
        "hometeam": hometeam,
        "homescore": homescore,
        "awayteam": awayteam,
        "awayscore": awayscore,
        "confidence": confidence,
        "totals": (homescore+awayscore),
        "spread": {
            "spreads": k,
            "counts": v,
        },
    }

    return values


k = 1

# montecarlo(0, 'Milwaukee Bucks', 'Charlotte Hornets', homeFactor=True)
