from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
from datetime import datetime, timedelta

schedule = pd.read_csv('NBA_Schedule_2023_24.csv')
    

def yesterdayGameData():

    today = datetime.today()
    d = today.strftime('%a, %b %d, %Y').replace(" 0", " ")

    yesterday = today - timedelta(1)
    yesterdayFormat2 = datetime.strftime(
        yesterday, '%a, %b %d, %Y').replace(" 0", " ")

    yesterdayGamesPlayed = schedule.loc[schedule['Date'] == yesterdayFormat2]
    return yesterdayGamesPlayed


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


def matchGameIds():
    yesterday = (
        datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    apiGames = leaguegamefinder.LeagueGameFinder(league_id_nullable='00')
    apiGames = apiGames.get_data_frames()[0]
    apiGames = apiGames[apiGames['GAME_DATE'] == yesterday]
    apiGamesIds = apiGames['GAME_ID'].unique()
    scheduleGame = yesterdayGameData()

    games = []
    for id in apiGamesIds:
        game = apiGames.groupby(['GAME_ID']).get_group(id)
        gameData = homeAway(game.values)
        homeTeam = gameData[0]
        if (gameData[0] == 'LA Clippers'):
            homeTeam= 'Los Angeles Clippers'
        if (gameData[0] == 'LA Lakers'):
            homeTeam = 'Los Angeles Clippers'
        scheduleGameIndex = scheduleGame[scheduleGame['Home/Neutral']
                                         == homeTeam].index[0]
        if (not scheduleGameIndex):
            continue
        game['GAME_ID'] = scheduleGameIndex
        games.append(game)
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
