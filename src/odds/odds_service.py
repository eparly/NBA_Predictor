from datetime import datetime, timedelta
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
            spread = response.json(
            )['results'][i]['odds'][0]['spread']['current']
            total = response.json()['results'][i]['odds'][0]['total']['current']
            
            moneyline_home = response.json(
            )['results'][i]['odds'][0]['moneyline']['current']['homeOdds']
            moneyline_home = self.american_to_int(moneyline_home)
            moneyline_away = response.json(
            )['results'][i]['odds'][0]['moneyline']['current']['awayOdds']
            moneyline_away = self.american_to_int(moneyline_away)
            hometeam = response.json()['results'][i]['teams']['home']['team']
            awayteam = response.json()['results'][i]['teams']['away']['team']
            game_odds = {
                'spreadHome': spread['home'],
                'spreadAway': spread['away'],
                'spreadHomeOdds': self.american_to_int(spread['homeOdds']),
                'spreadAwayOdds': self.american_to_int(spread['awayOdds']),
                'total': total['total'],
                'totalOver': self.american_to_int(total['overOdds']),
                'totalUnder': self.american_to_int(total['underOdds']),
                'home_ml': moneyline_home,
                'away_ml': moneyline_away,
                'hometeam': hometeam,
                'awayteam': awayteam,
            }
            print(game_odds)
            odds_data.append(game_odds)
        matched_order = self.match_order(odds_data, predictions)
        filtered_odds_data = [game for game in odds_data if (game['hometeam'], game['awayteam']) in {(pred['hometeam'], pred['awayteam']) for pred in predictions}]


        ordered_odds = []
        for i in range(len(matched_order)):
            print(filtered_odds_data[i])
            odds = {
                'date': self.date,
                'type-gameId': f"odds::{matched_order[i]}",
                'hometeam': filtered_odds_data[i]['hometeam'],
                'awayteam': filtered_odds_data[i]['awayteam'],
                'spreadHome': str(filtered_odds_data[i]['spreadHome']),
                'spreadAway': str(filtered_odds_data[i]['spreadAway']),
                'spreadHomeOdds': str(filtered_odds_data[i]['spreadHomeOdds']),
                'spreadAwayOdds': str(filtered_odds_data[i]['spreadAwayOdds']),
                'total': str(filtered_odds_data[i]['total']),
                'totalOver': str(filtered_odds_data[i]['totalOver']),
                'totalUnder': str(filtered_odds_data[i]['totalUnder']),
                'home_ml': str(filtered_odds_data[i]['home_ml']),
                'away_ml': str(filtered_odds_data[i]['away_ml']),
            }
            ordered_odds.append(odds)
            print(odds)
            self.dynamoDbService.create_item(odds)
        return ordered_odds
            
    def match_order(self, odds_data, predictions):
        # odds_data = np.array(odds_data)
        team_pair_to_index = {
            (pred['hometeam'], pred['awayteam']): pred['type-gameId'].split('::')[1]
            for idx, pred in enumerate(predictions)
        }
        
        indexed_odds_data = []
        for game in odds_data:
            team_pair = (game['hometeam'], game['awayteam'])
            if team_pair in team_pair_to_index:
                indexed_odds_data.append((team_pair_to_index[team_pair]))
            else:
                print('game not found', {team_pair})
        sorted_odds_data = np.array([game_id for game_id in indexed_odds_data])
        
        return sorted_odds_data
    
    def american_to_int(self, american_odds):
        if american_odds < 0:
            int_odds = -100 / american_odds + 1
        else:
            int_odds = american_odds / 100 + 1

        return round(int_odds, 2)
    
    # functions used to get odds from previous days
    def generate_date_range(self, start_date: str, end_date: str):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        delta = timedelta(days=1)
        current = start
        dates = []
        while current <= end:
            dates.append(current.strftime('%Y-%m-%d'))
            current += delta
        return dates
    
    def run_for_date(self, date: str):
        self.date = date
        self.get_odds()
    
    def run_odds_service_for_date_range(self, start_date: str, end_date: str):
        # dates = ['2024-10-28,2024-11-09', '2024-11-10,2024-11-22', '2024-11-23,2024-12-07', '2024-12-08,2024-12-17']
        dates = self.generate_date_range(start_date, end_date)
        url = "https://sportspage-feeds.p.rapidapi.com/games"
        querystring = {"league": "NBA", "date": f"{start_date},{end_date}"}
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "sportspage-feeds.p.rapidapi.com"
        }
        self.response = requests.get(url, headers=headers, params=querystring)
        for date in dates:
            print('running for date', date)
            self.run_for_date(date)   
    