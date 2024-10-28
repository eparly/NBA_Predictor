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
        prediction = montecarlo(game_id, home_team, away_team, nba_api_service=self.nba_api_service)
        print(prediction)
        return prediction
        
    