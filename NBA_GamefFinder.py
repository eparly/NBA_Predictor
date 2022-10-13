#nba game finder
import pandas as pd
from datetime import datetime
today=datetime.today()
schedule=pd.read_excel(r'NBA_2023_schedule.xlsx')

d=today.strftime('%a, %b %d, %Y').replace(" 0", " ")
i=1
n=0
while (1):
     
     if schedule.at[i, "Date"]==d:
         print(schedule.at[i, "Visitor/Neutral"], ',', schedule.at[i, "Home/Neutral"] )
         
         n+=1
         if n>14:
             break
     if n>0 and schedule.at[i, "Date"]!=d:
         
         break
     
     i+=1
     
     








