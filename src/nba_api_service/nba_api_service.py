from nba_api.stats.endpoints import leaguedashptteamdefend, leaguegamefinder
from nba_api.stats.endpoints import leaguedashteamstats, teamdashptshots, leaguedashoppptshot
from nba_api.stats.static import teams

import time as t
import pandas as pd

class NBAApiService:
    def __init__(self, N: int, proxy: str):
        self.proxy = proxy
        self.N = N
        
        
    def getResults(self):
        games = leaguegamefinder.LeagueGameFinder(proxy=self.proxy, league_id_nullable='00')
        return games
        
    def teamID(self, teamname, teams):
        teams = teams.get_teams()
        ID = [x for x in teams if x['full_name'] == teamname][0]
        ID = ID['id']
        return ID
    
    def offense_stats(self, teamname):
        teamstat = teamdashptshots.TeamDashPtShots(proxy=self.proxy, team_id = self.teamID(teamname, teams), last_n_games=self.N, 
            per_mode_simple="PerGame").get_data_frames()[0]

        free_throws = leaguedashteamstats.LeagueDashTeamStats(
            proxy=self.proxy, team_id_nullable=self.teamID(teamname, teams), last_n_games=self.N, per_mode_detailed="PerGame"
            ).get_data_frames()[0][['FTA', 'FT_PCT']]
        teamstat['FTA'] = free_throws['FTA']
        teamstat['FT_PCT'] = free_throws['FT_PCT']
        # if (len(teamstat)==0):
        #     teamstat = leaguedashteamstats.LeagueDashTeamStats(
        #         team_id_nullable=teamID(teamname, teams), per_mode_detailed="PerGame").get_data_frames()[0]
        return teamstat


    def defense_stats(self, teamname):
        teamstat = leaguedashoppptshot.LeagueDashOppPtShot(proxy=self.proxy, team_id_nullable=self.teamID(teamname, teams),
            last_n_games_nullable=self.N, per_mode_simple="PerGame").get_data_frames()[0]
                

        # teamstat = leaguedashptteamdefend.LeagueDashPtTeamDefend(team_id_nullable=teamID(
        #     teamname, teams), last_n_games_nullable=N, location_nullable=location, per_mode_simple="PerGame").get_data_frames()[0]
        return teamstat

    # This is probably not used
    def defense_3stats(self, teamname):
        try:
            teamstat = leaguedashptteamdefend.LeagueDashPtTeamDefend(proxy=self.proxy, defense_category='3 Pointers', team_id_nullable=self.teamID(
                teamname, teams), last_n_games_nullable=self.N, per_mode_simple="PerGame").get_data_frames()[0]
        except:
            teamstat = leaguedashptteamdefend.LeagueDashPtTeamDefend(proxy=self.proxy, defense_category='3 Pointers', team_id_nullable=self.teamID(
                teamname, teams), per_mode_simple="PerGame").get_data_frames()[0]
        return teamstat

    #this is probably not used - update basketball5_2.py to use it
    def get_data(self, hometeam, awayteam, D):

        # offense factor: how much the defensive stats impact average stats
        O = 1-D

        O_H = self.offense_stats(hometeam)
        t.sleep(.6)
        D_H = self.defense_stats(hometeam)
        t.sleep(.6)
        D3_H = self.defense_3stats(hometeam)
        t.sleep(.6)

        O_A = self.offense_stats(awayteam)
        t.sleep(.6)

        D_A = self.defense_stats(awayteam)
        t.sleep(.6)

        D3_A = self.defense_3stats(awayteam)
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
            'reb_a': O_H['REB']/self.N,
            'stl_a': O_H['STL']/self.N,
            'blk_a': O_H['BLK']/self.N,
            'tov_a': O_H['TOV']/self.N,
            'home_a': 1,
            'fgp_b': fgp_b,
            'fga_b': O_A['FGA'],
            'fg3_b': tfgp_b,
            'ftp_b': ft_p_b,
            'reb_b': O_A['REB']/self.N,
            'stl_b': O_A['STL']/self.N,
            'blk_b': O_A['BLK']/self.N,
            'tov_b': O_A['TOV']/self.N,
            'home_b': 0,
        }

        stats = pd.DataFrame(stats)

        return stats
