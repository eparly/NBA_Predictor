from nba_api.stats.endpoints import leaguegamefinder
import mysql.connector
from dotenv import load_dotenv
import os 

load_dotenv()
DB_PASS = os.environ.get('DB_PASS')
connection = mysql.connector.connect(
        host='localhost', database='nba_23_24', user='root', password=DB_PASS)

a = leaguegamefinder.LeagueGameFinder(
    league_id_nullable='00')


games = a.get_data_frames()[0]
games = games[games.SEASON_ID.str[-4:] >= '2015']
games = games.dropna(axis='rows')

games["HOME"] = games.loc[games["MATCHUP"].str.contains(
    '@'), "MATCHUP"].apply(lambda x: 0)
games["HOME"] = games["HOME"].fillna(1)

games = games.drop(columns=['SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION',
                   'TEAM_NAME', 'GAME_DATE', 'MATCHUP', 'MIN'])
k = 0


def set_historic():

    for i in range(10, 30000):
        insert_historic(i)


def insert_historic(i):
    
    cursor = connection.cursor()
    sql = "INSERT INTO historic(game_id, PTS, FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT, FTM, FTA, FT_PCT, OREB, DREB, REB, AST, STL, BLK, TOV, PF, PLUS_MINUS, WL, HOME)VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    values = games[i:i+1].values[0]
    cursor.execute(sql, (values[0], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10],
                         values[11], values[12], values[13], values[14], values[15], values[16], values[17], values[18], values[19], values[20], values[1], values[21]))

    connection.commit()


