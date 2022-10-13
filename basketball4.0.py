#retired
#=============================================
#outright winners: 93/146=63.7%
#=============================================
#spreads: 59/99=59.6%
#=============================================



#pull data using nba api
from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguedashptteamdefend

#set number of games for data used
N=10

#find team data
def teamID(teamname, teams):
    
    teams = teams.get_teams()
    ID = [x for x in teams if x['abbreviation']==teamname][0]
    ID = ID['id']
    return ID

#gathering team stats
def offense_stats(teamname):
    
    teamstat=leaguedashteamstats.LeagueDashTeamStats(team_id_nullable=teamID(teamname, teams), last_n_games=N).get_data_frames()[0]   
    return teamstat

def defense_stats(teamname):
    teamstat=teamstat_def=leaguedashptteamdefend.LeagueDashPtTeamDefend(team_id_nullable=teamID(teamname, teams), last_n_games_nullable=N).get_data_frames()[0]
    return teamstat

#generating points using data, based on expected shots made
def points(hometeam, awayteam):
    O=offense_stats(hometeam)
    D=defense_stats(awayteam)
    
    #calculating 2 pointers made
    fgm=(((O['FGA']-O['FG3A']+D['D_FGA']-(32*N))/(2*N))*(O['FG_PCT']+D['D_FG_PCT'])/2)
    
    #claculating 3 pointers made
    fg3m=(((O['FG3A']+D['D_FGA']-(32*N))/(2*N))*(O['FG3_PCT']+D['D_FG_PCT']-0.12)/2)
    
    #calculating ftm
    ftm=(O['FTA']/N)*(O['FT_PCT'])
    
    #calculating turnover points lost/generated
    #unused, but still iinteresting, with more fine tuning could be successful
    stl_pts_g=defense_impact(awayteam, hometeam)
    stl_pts_l=defense_impact(hometeam, awayteam)
    
    #expected score points
    return (2*fgm)+(3*fg3m)+ftm
     

#attempt to measure defenses imoact on turning turnovers into additional points
def defense_impact(hometeam, awayteam):
    #hometeam is on offense
    O=offense_stats(hometeam)
    D=offense_stats(awayteam)
    
    #calculating points lost on turnovers
    pLoss=(D['STL']+D['BLK'])*O['FG_PCT']/N
    
    return pLoss
    
#loop to enter in teams 
hometeam=''
while(hometeam!='END'):
    hometeam=input('enter home team name')
    awayteam=input('enter away team name')
    
    
    P_home=points(hometeam, awayteam)
    P_away=points(awayteam, hometeam)
    
    
    print(hometeam, P_home[0])
    
    print(awayteam, P_away[0])



