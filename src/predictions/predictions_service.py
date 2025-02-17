from datetime import datetime, timedelta
import json
import boto3
import dateutil.tz
from dynamodb.dynamoDbService import DynamoDBService
from nba_api_service.nba_api_service import NBAApiService
from predictions.basketball5_2 import montecarlo
from s3.s3Service import S3Service
from utils.getSecret import get_secret


class PredictionService:
    def __init__(self, dynamoDbService: DynamoDBService, s3Service: S3Service, sqs_queue_url: str, nba_api_service: NBAApiService):
        self.dynamoDbService = dynamoDbService
        self.s3Service = s3Service
        self.sqs_queue_url = sqs_queue_url
        self.sqs_client = boto3.client('sqs')
        eastern = dateutil.tz.gettz('US/Eastern')
        date = datetime.now(tz = eastern)
        self.str_date = date.strftime('%Y-%m-%d')
        self.nba_api_service = nba_api_service
      
    def start(self):
        print('Starting predictions')
        schedule = self.s3Service.get_schedule()
        eastern = dateutil.tz.gettz('US/Eastern')

        today = (datetime.now(tz = eastern)).strftime('%a %b %d %Y').replace(" 0", " ")
        
        todayGames = schedule.loc[schedule['Date'] == today]
        
        for index, row in todayGames.iterrows():
            game_id = index
            home_team = row['Home/Neutral']
            away_team = row['Visitor/Neutral']
            self.send_to_sqs(game_id, home_team, away_team)
            
    def send_to_sqs(self, game_id, home_team, away_team):
        message_body = {
            'game_id': game_id,
            'home_team': home_team,
            'away_team': away_team
        }
        response = self.sqs_client.send_message(
            QueueUrl = self.sqs_queue_url,
            MessageBody = json.dumps(message_body)
        )
        print(response)
        return response
    
    def predict(self, game_id, home_team, away_team):
        print('Predicting game', game_id, home_team, away_team)
        O_H = self.nba_api_service.offense_stats(home_team).loc[0]
        D_H = self.nba_api_service.defense_stats(home_team)

        O_A = self.nba_api_service.offense_stats(away_team).loc[0]
        D_A = self.nba_api_service.defense_stats(away_team)
        
        # Make a copy with float values converted to strings for storage
        O_H_str = self.convert_floats_to_strings(O_H.to_dict())
        D_H_str = self.convert_floats_to_strings(D_H.to_dict())
        O_A_str = self.convert_floats_to_strings(O_A.to_dict())
        D_A_str = self.convert_floats_to_strings(D_A.to_dict())
        self.store_pregame(game_id, home_team, O_H_str, D_H_str, 'home')
        self.store_pregame(game_id, away_team, O_A_str, D_A_str, 'away')
        prediction = montecarlo(game_id, home_team, away_team, O_H, O_A, D_H, D_A, nba_api_service=self.nba_api_service)
        print(prediction)
        return prediction
    
    def convert_floats_to_strings(self, data):
        if isinstance(data, dict):
            return {str(k): self.convert_floats_to_strings(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert_floats_to_strings(v) for v in data]
        elif isinstance(data, float):
            return str(data)
        else:
            return data
    
    def store_pregame(self, game_id, teamname, offense, defense, location):
        item = {
            'date': self.str_date,
            'type-gameId': f"pregame::{game_id}::{teamname}",
            'location': location,
            'offense': offense,
            'defense': defense
        }
        print(item)
        self.dynamoDbService.create_item(item)
        return item
        
    