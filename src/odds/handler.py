import json
from dynamodb.dynamoDbService import DynamoDBService
from odds.odds_service import OddsService
from s3.s3Service import S3Service
import os

from utils.getSecret import get_secret

tableName = os.getenv('tableName')
bucketName = os.getenv('bucketName')
def lambda_handler(event, context):
    secret = get_secret('odds_api_key')
    api_key = json.loads(secret)['api_key']
    dynamoDbService = DynamoDBService(tableName)
    s3Service = S3Service(bucketName)
    odds_service = OddsService(api_key=api_key, 
                               url = "https://sportspage-feeds.p.rapidapi.com/games",
                               s3Service = s3Service,
                               dynamoDbService = dynamoDbService)
    response = odds_service.get_odds()
    # response = odds_service.run_odds_service_for_date_range('2024-12-21', '2024-12-23')
    print(response)
    return response