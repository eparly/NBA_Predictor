from collections import Counter
import math
import random as r
from nba_api_service.nba_api_service import NBAApiService


def montecarlo(gameID, hometeam, awayteam, homeFactor=False, multiplier=[1.0, 1.0], streak_mode = 'none', nba_api_service: NBAApiService = None):
    home = ''
    away = ''
    global N
    N = 5

    if homeFactor:
        home = 'Home'
        away = 'Road'
        N = 5
    
    home_streak_multiplier = 1.0
    away_streak_multiplier = 1.0
    if streak_mode == 'multiplier':
        home_streak_multiplier = multiplier[0]
        away_streak_multiplier = multiplier[1]
    elif streak_mode == 'factor': 
        home_streak_multiplier = multiplier[0]
        away_streak_multiplier = multiplier[1]
        #TODO - normalize factors to 1
        home_streak_multiplier = (home_streak_multiplier-away_streak_multiplier)*home_streak_multiplier + home_streak_multiplier
        away_streak_multiplier = (away_streak_multiplier-home_streak_multiplier)*away_streak_multiplier + away_streak_multiplier
        
    
    O_H = nba_api_service.offense_stats(hometeam, home).loc[0]
    D_H = nba_api_service.defense_stats(hometeam, home)
    # D3_H = defense_3stats(hometeam, home)

    O_A = nba_api_service.offense_stats(awayteam, away).loc[0]
    D_A = nba_api_service.defense_stats(awayteam, away)
    # D3_A = defense_3stats(awayteam, away)
    # calculating 2 pointers home
    fga_a = (O_H['FG2A']+D_A['FG2A'])/2
    

    # Use teamdashptshots - general shooting (dataset at index 3?)
    # for defense use LeagueDashOppPtShot

    fgp_a = (O_H['FG2_PCT']+D_A['FG2_PCT'])/2

    # claculating 3 pointers made home
    tfga_a = (O_H['FG3A']+D_A['FG3A'])/2
    tfgp_a = (O_H['FG3_PCT']+D_A['FG3_PCT'])/2

    # calculating ftm home
    fta_a = O_H['FTA']
    ft_p_a = O_H['FT_PCT']

    # calculating 2 pointers away
    fga_b = (O_A['FG2A']+D_H['FG2A'])/2
    fgp_b = (O_A['FG2_PCT']+D_H['FG2_PCT'])/2

    # claculating 3 pointers made away
    tfga_b = (O_A['FG3A']+D_H['FG3A'])/2
    tfgp_b = (O_A['FG3_PCT']+D_H['FG3_PCT'])/2

    # calculating ftm away
    fta_b = O_A['FTA']
    ft_p_b = O_A['FT_PCT']
    if(len(D_A)<1 or len(D_H) <1):
        return []
    if(D_A['GP'].values[0] <= 1 or D_H['GP'].values[0] <= 1):
        return []

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
        for i in range(int(fta_a)):
            n = r.random()
            if n < ft_p_a:
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
        for i in range(int(fta_b)):
            n = r.random()
            if n < ft_p_b:
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

    homescore_adjusted = homescore*home_streak_multiplier/(games)
    awayscore_adjusted = awayscore*away_streak_multiplier/(games)


    # results
    spreads = Counter(sorted(spread))
    k = list(spreads.keys())
    v = list(spreads.values())
    values = {
        "gameID": gameID,
        "hometeam": hometeam,
        "homescore": homescore_adjusted,
        "awayteam": awayteam,
        "awayscore": awayscore_adjusted,
        "confidence": confidence,
        "totals": (homescore_adjusted+awayscore_adjusted),
        "spread": {
            "spreads": k,
            "counts": v,
        },
    }

    return values

