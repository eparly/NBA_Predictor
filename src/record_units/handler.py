import os
from .record import RecordService
from dynamodb.dynamoDbService import DynamoDBService
from s3.s3Service import S3Service

tableName = os.getenv('tableName')
bucketName = os.getenv('bucketName')
def lambda_handler(event, context):
    dynamoDbService = DynamoDBService(tableName)
    recordService = RecordService(dynamoDbService)
    ev_threshold = 0.5  # Default threshold is 0.05
    response = recordService.test_ev_picks("2024-10-28", "2025-04-13", ev_threshold)
    # response = recordService.run_picks_service_for_date_range('2025-01-07', '2025-01-08')
    return response