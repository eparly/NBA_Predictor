import os

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


tableName = os.getenv('tableName')
def lambda_handler(event, context):
    # Initialize DynamoDB
    dynamodb = boto3.resource('dynamodb')
    season = event.get('season', 1)  # Default to season 1 if not provided
    table = dynamodb.Table(tableName)

    # Scan the table to get all items
    try:
        response = table.scan()
        items = response.get('Items', [])
        print(f"Found {len(items)} items in the table.")

        # Update each item to include the 'season' attribute
        for item in items:
            key = {key_attr['AttributeName']: item[key_attr['AttributeName']] for key_attr in table.key_schema}
            print(f"Updating item with key: {key}")

            table.update_item(
                Key=key,
                UpdateExpression="SET #season = :season",
                ExpressionAttributeNames={
                    '#season': 'season'
                },
                ExpressionAttributeValues={
                    ':season': season
                }
            )
        print(f"Migration complete. All items updated with season {season}.")
        return {"statusCode": 200, "body": f"Migration complete. Updated {len(items)} items with season {season}."}

    except ClientError as e:
        print(f"Error during migration: {e}")
        return {"statusCode": 500, "body": f"Error during migration: {e}"}