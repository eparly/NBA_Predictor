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
        inverse_edge=4.0,
    )
    # response = picks_service.value_picks()
    # response = picks_service.spread_picks()
    # response = picks_service.run_picks_service_for_date_range('2024-10-29', '2024-12-25')
    response = picks_service.all_picks()
    return response