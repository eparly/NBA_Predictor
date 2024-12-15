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
    return response