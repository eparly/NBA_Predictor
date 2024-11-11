from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
from datetime import datetime, timedelta
import json
import dateutil.tz
from nba_api_service.nba_api_service import NBAApiService
from utils.getSecret import get_secret
from s3.s3Service import S3Service
from dynamodb.dynamoDbService import DynamoDBService

class GameResultsService:
    def __init__(self, s3Service: S3Service, dynamoDbService: DynamoDBService, nbaApiService: NBAApiService):
        self.s3Service = s3Service
        self.dynamoDbService = dynamoDbService
        eastern = dateutil.tz.gettz('US/Eastern')
        self.date = datetime.now(tz = eastern)
        self.nbaApiService = nbaApiService

    def yesterdayGameData(self):

        schedule = self.s3Service.get_schedule()

        yesterday = self.date - timedelta(1)
        yesterdayFormat2 = datetime.strftime(
            yesterday, '%a %b %d %Y').replace(" 0", " ")


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

    def matchGameIds(self):
        games = self.nbaApiService.getResults()
        apiGames = games.get_data_frames()[0]
        yesterday = (self.date - timedelta(1)).strftime('%Y-%m-%d')
        apiGames = apiGames[apiGames['GAME_DATE'] == yesterday]
        apiGamesIds = apiGames['GAME_ID'].unique()
        scheduleGame = self.yesterdayGameData()
        if (scheduleGame.size <= 0):
            return []
        games = []
        for id in apiGamesIds:
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
                print('ERROR')
                n+=1
                continue
            if (not scheduleGameIndex):
                continue
            try:
                game['GAME_ID'] = scheduleGameIndex
                games.append(game)
            except:
                continue
        return games

    def gameResults(self, games):
        game = games[0:2].values
        hometeam, awayteam, homescore, awayscore, gameID = self.homeAway(game)
        dateString = (self.date-timedelta(1)).strftime('%Y-%m-%d')
        values = {
            "date": dateString,
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
