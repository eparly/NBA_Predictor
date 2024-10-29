from datetime import datetime
import dateutil.tz
import numpy as np
import requests
from dynamodb.dynamoDbService import DynamoDBService
from s3.s3Service import S3Service


class OddsService:
    def __init__(self, api_key: str, url: str, s3Service: S3Service, dynamoDbService: DynamoDBService):
        self.api_key = api_key
        self.url = url
        self.s3Service = s3Service
        self.dynamoDbService = dynamoDbService
        eastern = dateutil.tz.gettz('US/Eastern')
        self.date = datetime.now(tz = eastern).strftime('%Y-%m-%d')
        
    
    def get_predictions(self):
        predictions = self.dynamoDbService.get_items_by_date_and_sort_key_prefix(self.date, 'predictions')
        return predictions
    
    def get_odds(self):
        predictions = self.get_predictions()
        url = "https://sportspage-feeds.p.rapidapi.com/games"
        querystring = {"league": "NBA"}
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "sportspage-feeds.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        games = len(response.json()['results'])

        # games from this api arent in the same order as the other one, need to enter these ones in the same order as we do for all predictions
        odds_data = []
        ml_data = []
        i = 0
        for i in range(games):
            if "odds" not in response.json()['results'][i]:
                return 'no odds yet, check back later'
            spreads = response.json(
            )['results'][i]['odds'][0]['spread']['current']['home']
            moneyline_home = response.json(
            )['results'][i]['odds'][0]['moneyline']['current']['homeOdds']
            moneyline_home = self.american_to_int(moneyline_home)
            moneyline_away = response.json(
            )['results'][i]['odds'][0]['moneyline']['current']['awayOdds']
            moneyline_away = self.american_to_int(moneyline_away)
            hometeam = response.json()['results'][i]['teams']['home']['team']
            awayteam = response.json()['results'][i]['teams']['away']['team']

            odds_data.append((spreads, hometeam, awayteam))
            ml_data.append((moneyline_home, moneyline_away, hometeam, awayteam))
            
        matched_order = self.match_order(odds_data, predictions)

        ordered_odds = []
        for i in range(len(matched_order)):
            odds = {
                'date': self.date,
                'type-gameId': f"odds::{matched_order[i]}",
                'hometeam': odds_data[i][1],
                'awayteam': odds_data[i][2],
                'spread': str(odds_data[i][0]),
                'home_ml': str(ml_data[i][0]),
                'away_ml': str(ml_data[i][1]),
            }
            ordered_odds.append(odds)
            self.dynamoDbService.create_item(odds)
        return ordered_odds
            
    def match_order(self, odds_data, predictions):
        odds_data = np.array(odds_data)
        predictions = np.array(predictions)

        game_order = []
        for j in range(len(odds_data)):
            game_id = [i for i in range(len(
                predictions)) if odds_data[:, 1:3][j][0] == predictions[i]['hometeam'] and odds_data[:, 1:3][j][1] == predictions[i]['awayteam']]
            print('game_id:', game_id)
            if len(game_id) == 0:
                continue
            game_id = predictions[game_id][0]['type-gameId'].split('::')[1]

            game_order.append(game_id)

        return game_order
    
    def american_to_int(self, american_odds):
        if american_odds < 0:
            int_odds = -100 / american_odds + 1
        else:
            int_odds = american_odds / 100 + 1

        return round(int_odds, 2)
    