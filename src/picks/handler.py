import os
from dynamodb.dynamoDbService import DynamoDBService
from picks.picks_service import PicksService

tableName = os.getenv('tableName')
queue_url = os.getenv('oddsQueueUrl')
def lambda_handler(event, context):
    dynamoDbService = DynamoDBService(tableName)
    picks_service = PicksService(
        dynamoDbService=dynamoDbService,
        edge=0.05,
        inverse_edge=3.0
    )
    response = picks_service.value_picks()
    return response