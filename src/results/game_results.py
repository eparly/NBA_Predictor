from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
from datetime import datetime, timedelta
import os

class GameResultsService:
    def __init__(self, s3Service, dynamoDbService):
        self.s3Service = s3Service
        self.dynamoDbService = dynamoDbService

        self.date = (
            datetime.now() - timedelta(200)).strftime('%Y-%m-%d')
        # self.PROXY = os.getenv('PROXY')
    def yesterdayGameData(self):

        schedule = self.s3Service.get_schedule()
        today = datetime.today()
        d = today.strftime('%a, %b %d, %Y').replace(" 0", " ")

        yesterday = today - timedelta(200)
        yesterdayFormat2 = datetime.strftime(
            yesterday, '%a, %b %d, %Y').replace(" 0", " ")

        yesterdayGamesPlayed = schedule.loc[schedule['Date'] == yesterdayFormat2]
        return yesterdayGamesPlayed


    def homeAway(self, game):
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
        a = leaguegamefinder.LeagueGameFinder(league_id_nullable='00',)
        games = a.get_data_frames()[0]
        games = games[games['GAME_DATE'] == yesterday]
        games = games['GAME_ID']
        games = games.values
        return games


    def matchGameIds(self):
        PROXY = "http://bihbbirx:19u2egbwdct9@64.64.118.149:6732"
        games = leaguegamefinder.LeagueGameFinder(proxy=PROXY, date_from_nullable='01/18/2024', date_to_nullable='01/18/2024')
        apiGames = games.get_data_frames()[0]
        print('success!!')
        apiGames = apiGames[apiGames['GAME_DATE'] == self.date]
        apiGamesIds = apiGames['GAME_ID'].unique()
        scheduleGame = self.yesterdayGameData()
        if (scheduleGame.size <= 0):
            return []
        print(scheduleGame)
        games = []
        for id in apiGamesIds:
            print(id)
            n=0
            game = apiGames.groupby(['GAME_ID']).get_group(id)
            gameData = self.homeAway(game.values)
            homeTeam = gameData[0]
            if (gameData[0] == 'LA Clippers'):
                homeTeam= 'Los Angeles Clippers'
            if (gameData[0] == 'LA Lakers'):
                homeTeam = 'Los Angeles Lakers'
            try:
                scheduleGameIndex = scheduleGame[scheduleGame['Home/Neutral']
                                                == homeTeam].index[0]
            except:
                n+=1
                continue
            if (not scheduleGameIndex):
                continue
            try:
                game['GAME_ID'] = scheduleGameIndex
                games.append(game)
            except:
                continue
        print(games)
        return games



    def pullGames(gameID):
        a = leaguegamefinder.LeagueGameFinder(league_id_nullable='00')
        games = a.get_data_frames()[0]
        games = games.dropna(axis='rows')
        games = games[games['GAME_ID'] == gameID]
        return games


    def gameResults(self, games):
        game = games[0:2].values
        hometeam, awayteam, homescore, awayscore, gameID = self.homeAway(game)
        values = {
            "date": self.date,
            "type-gameId": f"results::{gameID}",
            "hometeam": hometeam,
            "homescore": homescore,
            "awayteam": awayteam,
            "awayscore": awayscore,
        }
        return values


    def results(self):
        today = datetime.today()
        values = 'No game played yesterday'
        gameData = self.matchGameIds()
        if (gameData == []):
            return values
        
        for game in gameData:
            values = self.gameResults(game)
            print(values)
            self.dynamoDbService.create_item(values)
        return values
    
a=0
