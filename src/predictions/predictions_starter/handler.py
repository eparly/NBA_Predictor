import os
import json

from dynamodb.dynamoDbService import DynamoDBService
from s3.s3Service import S3Service
from ..predictions_service import PredictionService
from utils.getSecret import get_secret
from nba_api_service.nba_api_service import NBAApiService

tableName = os.getenv('tableName')
bucketName = os.getenv('bucketName')
predictionQueueUrl = os.getenv('predictionQueueUrl')


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
    nba_api_service = NBAApiService(N=10, proxy=proxy)
    
    predictionService = PredictionService(dynamoDbService, s3Service, predictionQueueUrl, nba_api_service)
    response = predictionService.start()
    return response