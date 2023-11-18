from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguedashptteamdefend

import time as t
import pandas as pd

N = 10

# defense factor: how much the defensive stats impact average stats
D = 0.3
O = 1-D


def teamID(teamname, teams):

    teams = teams.get_teams()
    ID = [x for x in teams if x['full_name'] == teamname][0]
    ID = ID['id']
    return ID
# calculate 2 pointers on average
# gathering team stats


def offense_stats(teamname):

    teamstat = leaguedashteamstats.LeagueDashTeamStats(
        team_id_nullable=teamID(teamname, teams), last_n_games=N).get_data_frames()[0]
    return teamstat


def defense_stats(teamname):
    teamstat = leaguedashptteamdefend.LeagueDashPtTeamDefend(team_id_nullable=teamID(
        teamname, teams), last_n_games_nullable=N).get_data_frames()[0]
    return teamstat


def defense_3stats(teamname):
    teamstat = leaguedashptteamdefend.LeagueDashPtTeamDefend(defense_category='3 Pointers', team_id_nullable=teamID(
        teamname, teams), last_n_games_nullable=N).get_data_frames()[0]
    return teamstat


def get_data(hometeam, awayteam, D):

    # offense factor: how much the defensive stats impact average stats
    O = 1-D

    O_H = offense_stats(hometeam)
    t.sleep(.6)
    D_H = defense_stats(hometeam)
    t.sleep(.6)
    D3_H = defense_3stats(hometeam)
    t.sleep(.6)

    O_A = offense_stats(awayteam)
    t.sleep(.6)

    D_A = defense_stats(awayteam)
    t.sleep(.6)

    D3_A = defense_3stats(awayteam)
    t.sleep(.6)

    # calculating 2 pointers home

    fgp_a = (O_H['FG_PCT']*O+D_A['D_FG_PCT']*D)

    tfgp_a = (O_H['FG3_PCT']*O+D3_A['FG3_PCT']*D)

    ft_p_a = O_A['FT_PCT']
    fgp_b = (O_A['FG_PCT']*O+D_H['D_FG_PCT']*D)

    tfgp_b = (O_A['FG3_PCT']*O+D3_H['FG3_PCT']*D)

    ft_p_b = O_A['FT_PCT']

    stats = {
        'fgp_a': fgp_a,
        'fga_a': O_H['FGA'],
        'fg3_a': tfgp_a,
        'ftp_a': ft_p_a,
        'reb_a': O_H['REB']/N,
        'stl_a': O_H['STL']/N,
        'blk_a': O_H['BLK']/N,
        'tov_a': O_H['TOV']/N,
        'home_a': 1,
        'fgp_b': fgp_b,
        'fga_b': O_A['FGA'],
        'fg3_b': tfgp_b,
        'ftp_b': ft_p_b,
        'reb_b': O_A['REB']/N,
        'stl_b': O_A['STL']/N,
        'blk_b': O_A['BLK']/N,
        'tov_b': O_A['TOV']/N,
        'home_b': 0,
    }

    stats = pd.DataFrame(stats)

    return stats
