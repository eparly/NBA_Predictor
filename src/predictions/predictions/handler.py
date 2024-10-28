from datetime import datetime
import os
import json
import boto3


from dynamodb.dynamoDbService import DynamoDBService
from nba_api_service.nba_api_service import NBAApiService
from predictions.basketball5_2 import montecarlo
from s3.s3Service import S3Service
from utils.getSecret import get_secret
from ..predictions_service import PredictionService
tableName = os.getenv('tableName')
bucketName = os.getenv('bucketName')
predictionQueueUrl = os.getenv('predictionQueueUrl')

sqs_client = boto3.client('sqs')

def lambda_handler(event, context):
    body = json.loads(event['Records'][0]['body'])
    print(body)
    game_id = body['game_id']
    home_team = body['home_team']
    away_team = body['away_team']
    
    proxyInfo = get_secret('proxy-credentials')
    proxyInfo = json.loads(proxyInfo)
    proxy_port = proxyInfo['proxy_port']
    proxy_username = proxyInfo['proxy_username']
    proxy_password = proxyInfo['proxy_password']
    proxy_host = proxyInfo['proxy_host']
    proxy = f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}'
    dynamoDbService = DynamoDBService(tableName)
    s3Service = S3Service(bucketName)
    nba_api_service = NBAApiService(N=2, proxy=proxy)
    
    predictionService = PredictionService(dynamoDbService, s3Service, predictionQueueUrl, nba_api_service)
    response = predictionService.predict(game_id, home_team, away_team)
    print('response', response)
    item = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type-gameId': f"predictions::{game_id}",
        'hometeam': home_team,
        'awayteam': away_team,
        'homescore': int(response['homescore']),
        'awayscore': int(response['awayscore']),
        'confidence': str(response['confidence'])
    }
    
    dynamoDbService.create_item(item)
    
    receipt_handle = event['Records'][0]['receiptHandle']
    sqs_client.delete_message(
        QueueUrl=predictionQueueUrl,
        ReceiptHandle=receipt_handle
    )
    return response