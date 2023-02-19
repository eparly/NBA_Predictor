from sqlite3 import connect
import mysql.connector
from dotenv import load_dotenv
import os 

load_dotenv()
DB_PASS = os.environ.get('DB_PASS')


connection = mysql.connector.connect(host='localhost',
                                     database='nba_predictor',
                                     user='root',
                                     password=DB_PASS)

def insert_predictions(values, table, date):

    cursor = connection.cursor()
    sql = f"INSERT IGNORE INTO {table}(game_id, Hometeam, Awayteam, Homescore, Awayscore, totals, date) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (values["gameID"], values["hometeam"], values["awayteam"],
                   values["homescore"], values["awayscore"], values["totals"], date))
    connection.commit()


def insert_spreads(spread, table, date):

    cursor = connection.cursor()
    sql = f"INSERT IGNORE INTO {table}(game_id, spread_home, spread_away, hometeam, awayteam, date) VALUES(%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (spread[0], spread[1],
                   spread[2], spread[3], spread[4], date))

    connection.commit()


def insert_scores(score, date):

    cursor = connection.cursor()
    cursor.execute(
        """INSERT IGNORE INTO scores(game_id, homescore, awayscore, hometeam, awayteam, date) VALUES(%s, %s, %s, %s, %s, %s)""", (score[0], score[1], score[2], score[3], score[4], date))

    connection.commit()


def get_predictions(table, gameID):

    cursor = connection.cursor()
    if gameID == "all":
        sql = f"SELECT * FROM {table}"
    else:
        sql = f"SELECT * FROM {table} WHERE game_id = {gameID}"
    cursor.execute(sql)
    result = cursor.fetchall()
    if result == []:
        return [(0, 0, 0, 0, 0, 0, 0)]
    return result


def get_results():
    
    cursor = connection.cursor()
    sql = f"SELECT * FROM game_results"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def insert_results(values, date):
    
    cursor = connection.cursor()

    cursor.execute("""INSERT IGNORE INTO game_results(game_id, hometeam, awayteam, homescore, awayscore, date)
						VALUES(%s, %s, %s, %s, %s, %s)""", (values["gameID"], values["hometeam"], values["awayteam"], values["homescore"], values["awayscore"], date))
    connection.commit()


def insert_record(date, score, table):

    cursor = connection.cursor()
    sql = f"INSERT IGNORE INTO {table}(date, correct, total) VALUES(%s, %s, %s)"
    cursor.execute(sql, (date, score["correct"], score["total"]))

    connection.commit()


def insert_factors(values, date):

    cursor = connection.cursor()

    cursor.execute("""INSERT IGNORE INTO factors(game_id, homescore, awayscore, hometeam, awayteam, date)
						VALUES(%s, %s, %s, %s, %s, %s)""", (values[0], values[1], values[2], values[3], values[4], date))
    connection.commit()


def get_historic():

    cursor = connection.cursor()
    sql = f"SELECT * FROM historic"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def insert_odds(values):

    cursor = connection.cursor()

    cursor.execute("""INSERT IGNORE INTO odds(game_id, spreads, hometeam, awayteam) VALUES(%s, %s, %s, %s)""", (
        values[0], values[1], values[2], values[3]))
    connection.commit()


def insert_spread_picks(values, table):

    cursor = connection.cursor()
    sql = f"INSERT IGNORE INTO {table}(game_id,teamname, pick) VALUES(%s, %s, %s)"
    cursor.execute(sql, (values[0], values[1], values[2]))
    connection.commit()


