from time import strftime
from nba_api.stats.endpoints import leaguegamefinder
import pymysql
from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(1)
yesterday = datetime.strftime(yesterday, '%Y-%m-%d')

a = leaguegamefinder.LeagueGameFinder(league_id_nullable='00')
games = a.get_data_frames()[0]
games = games.dropna(axis='rows')


def homeAway(game):
    if '@' in game[0][6]:
        hometeam = game[1][3]
        awayteam = game[0][3]
        homescore = game[1][9]
        awayscore = game[0][9]
    else:
        hometeam = game[0][3]
        awayteam = game[1][3]
        homescore = game[0][9]
        awayscore = game[1][9]
    gameID = game[0][4]
    return hometeam, awayteam, homescore, awayscore, gameID
# a.get_data_frames()[0][a.get_data_frames()[
    # 0]['GAME_DATE'] == yesterday][0]['GAME_ID']


def yesterdayGames(yesterday):
    a = leaguegamefinder.LeagueGameFinder(league_id_nullable='00')
    games = a.get_data_frames()[0]
    games = games[games['GAME_DATE'] == yesterday]
    games = games['GAME_ID']
    games = games.values
    return games


def pullGames(gameID):
    a = leaguegamefinder.LeagueGameFinder(league_id_nullable='00')
    games = a.get_data_frames()[0]
    games = games.dropna(axis='rows')
    games = games[games['GAME_ID'] == gameID]
    return games


def gameResults(games):
    if games.size <= 0:
        return 'No games'
    game = games[0:2].values
    hometeam, awayteam, homescore, awayscore, gameID = homeAway(game)
    values = {
        "gameID": gameID,
        "hometeam": hometeam,
        "homescore": homescore,
        "awayteam": awayteam,
        "awayscore": awayscore,
    }
    return values


# first, last = firstLast(yesterday)
# b = gameResults(pullGames(first))
# c = 0
