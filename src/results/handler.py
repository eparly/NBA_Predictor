import os
from .game_results import GameResultsService
from dynamodb.dynamoDbService import DynamoDBService
from s3.s3Service import S3Service

tableName = os.getenv('tableName')
bucketName = os.getenv('bucketName')
def lambda_handler(event, context):
    # message = 'Hello {} {}!'.format(event['first_name'], event['last_name']) 
    # print(response)
    dynamoDbService = DynamoDBService(tableName)
    s3Service = S3Service(bucketName)
    gameResultsService = GameResultsService(s3Service, dynamoDbService)
    response = gameResultsService.results()
    return response