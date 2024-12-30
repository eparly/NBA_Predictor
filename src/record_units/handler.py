import os
from .record import RecordService
from dynamodb.dynamoDbService import DynamoDBService
from s3.s3Service import S3Service

tableName = os.getenv('tableName')
bucketName = os.getenv('bucketName')
def lambda_handler(event, context):
    dynamoDbService = DynamoDBService(tableName)
    recordService = RecordService(dynamoDbService)
    response = recordService.update_all_records()
    # response = recordService.run_picks_service_for_date_range('2024-12-27', '2024-12-30')
    return response