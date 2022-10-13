#==========================================
#overall 249/355
#spread 199/355
#totals 195/355



#import team data


from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguedashptteamdefend
import random as r
import time
from matplotlib import pyplot as plt


import pandas as pd
from datetime import datetime
today=datetime.today()
schedule=pd.read_excel(r'NBA_2023_schedule.xlsx')

d=today.strftime("%a, %b %d, %Y").replace(" 0", " ")


t=time
c=0
n=0
over=0
under=0
N=20
def teamID(teamname, teams):
    
    teams = teams.get_teams()
    ID = [x for x in teams if x['abbreviation']==teamname][0]
    ID = ID['id']
    return ID
#calculate 2 pointers on average
#gathering team stats
def offense_stats(teamname):
    
    teamstat=leaguedashteamstats.LeagueDashTeamStats(team_id_nullable=teamID(teamname, teams), last_n_games=N).get_data_frames()[0]   
    return teamstat

def defense_stats(teamname):
    teamstat=leaguedashptteamdefend.LeagueDashPtTeamDefend(team_id_nullable=teamID(teamname, teams), last_n_games_nullable=N).get_data_frames()[0]
    return teamstat

def defense_3stats(teamname):
    teamstat=leaguedashptteamdefend.LeagueDashPtTeamDefend(defense_category='3 Pointers', team_id_nullable=teamID(teamname, teams), last_n_games_nullable=N).get_data_frames()[0]
    return teamstat



def montecarlo(awayteam,hometeam,):
   O_H=offense_stats(hometeam)
   D_H=defense_stats(hometeam)
   D3_H=defense_3stats(hometeam)
   
   O_A=offense_stats(awayteam)
   D_A=defense_stats(awayteam)
   D3_A=defense_3stats(awayteam)
   #calculating 2 pointers home
   fga_a=(O_H['FGA']-O_H['FG3A']+D_A['D_FGA']-D3_A['FG3A'])/(2*N)
   time.sleep(1)
   fgp_a=(O_H['FG_PCT']+D_A['D_FG_PCT'])/2
   t.sleep(1) 
   
   #claculating 3 pointers made home
   tfga_a=(O_H['FG3A']+D_A['D_FGA']-D3_A['FG3A'])/(2*N)
   t.sleep(1)
   tfgp_a=(O_H['FG3_PCT']+D3_A['FG3_PCT'])/2
   t.sleep(1)
    
   #calculating ftm home
   fta_a=O_H['FTA']/N
   t.sleep(1)
   ft_p_a=O_A['FT_PCT']
   t.sleep(1)
   
   #calculating 2 pointers away
   fga_b=(O_A['FGA']-O_A['FG3A']+D_H['D_FGA']-D3_H['FG3A'])/(2*N)
   t.sleep(1)
   fgp_b=(O_A['FG_PCT']+D_H['D_FG_PCT'])/2
   t.sleep(1)
    
   #claculating 3 pointers made away
   tfga_b=((O_A['FG3A']+D_H['D_FGA']-D3_H['FG3A'])/(2*N))
   t.sleep(1)
   tfgp_b=(O_A['FG3_PCT']+D3_H['FG3_PCT'])/2
   t.sleep(1)
    
   #calculating ftm away
   fta_b=O_A['FTA']/N
   t.sleep(1)
   ft_p_b=O_A['FT_PCT']
   t.sleep(1)
   
   
   c=0
   d=0
  
   games=1000
   homescore=0
   awayscore=0
   pointsA=0
   pointsB=0
   d=0
   spread=[]
   totals=[]
   for j in range(games):
       pointsA=0
       pointsB=0
       #simulating 2 point shots
       for i in range(int(fga_a[0])):
           n=r.random()
           if n<fgp_a[0]:
               pointsA+=2
       #simulating 3 point shots
       for i in range (int(tfga_a[0])):
           n=r.random()
           if n<tfgp_a[0]:
               pointsA+=3
             #simulating free throws
       for i in range(int(fta_a[0])):
           n=r.random()
           if n< ft_p_a[0]:
               pointsA+=1
       
       
       #simulating 2 point shots
       for i in range(int(fga_b[0])):
           n=r.random()
           if n<fgp_b[0]:
               pointsB+=2
       #simulating 3 point shots
       for i in range (int(tfga_b[0])):
           n=r.random()
           if n<tfgp_b[0]:
               pointsB+=3
             #simulating free throws
       for i in range(int(fta_b[0])):
           n=r.random()
           if n< ft_p_b[0]:
               pointsB+=1
       totals.append(pointsA+pointsB)
       spread.append(pointsA-pointsB)
       homescore+=pointsA
       awayscore+=pointsB
       if pointsA>pointsB:
           c+=1
       if pointsB>pointsA:
           d+=1
       if pointsA==pointsB:
           d+=1
   plt.figure(1)
   plt.hist(totals, bins= 100)
   plt.figure(2)
   plt.hist(spread, bins=100)
   plt.show()
   if c>d:
      confidence=c/(games)
   if d>c:
       confidence=d/(games)  
   if c==d:
       confidence=0.5
 
   homescore=homescore/(games)
   awayscore=awayscore/(games)
   
   
   #results
   print(awayteam,awayscore, hometeam,homescore,)
   
   return round(confidence*100, 2)
          
       
   
 
'''  
i=0
n=0
while (1):
     
     if schedule.at[i, "Date"]==d:
         print(montecarlo(schedule.at[i, "Visitor/Neutral"], schedule.at[i, "Home/Neutral"]))
         n+=1
         if n>14:
             break
     if n>0 and schedule.at[i,"Date"]!=d:
         break
     i+=1 

#tests against a large sample of games
'''

hometeam=''
while(hometeam!='END'):
    hometeam=input('enter home team name')
    awayteam=input('enter away team name')
    print(montecarlo(hometeam, awayteam))



