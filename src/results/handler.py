import json
import os
from nba_api_service.nba_api_service import NBAApiService
from utils.getSecret import get_secret
from .game_results import GameResultsService
from dynamodb.dynamoDbService import DynamoDBService
from s3.s3Service import S3Service

tableName = os.getenv('tableName')
bucketName = os.getenv('bucketName')
def lambda_handler(event, context):
    proxyInfo = get_secret('proxy-credentials')
    proxyInfo = json.loads(proxyInfo)
    proxy_port = proxyInfo['proxy_port']
    proxy_username = proxyInfo['proxy_username']
    proxy_password = proxyInfo['proxy_password']
    proxy_host = proxyInfo['proxy_host']
    proxy = f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}'
    dynamoDbService = DynamoDBService(tableName)
    s3Service = S3Service(bucketName)
    nbaApiService = NBAApiService(N = 10, proxy = proxy)
    gameResultsService = GameResultsService(s3Service, dynamoDbService, nbaApiService)
    response = gameResultsService.results()
    return response