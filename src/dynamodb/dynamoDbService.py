import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from boto3.dynamodb.conditions import Key, Attr


class DynamoDBService:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def write_item(self, item):
        try:
            self.table.put_item(Item=item)
            print(f"Item {item} written to table {self.table.name}")
        except NoCredentialsError:
            print("Credentials not available")
        except ClientError as e:
            print(f"Error writing item: {e}")

    def read_item(self, key):
        try:
            response = self.table.get_item(Key=key)
            if 'Item' in response:
                return response['Item']
            else:
                print(f"Item with key {key} not found in table {self.table.name}")
                return None
        except NoCredentialsError:
            print("Credentials not available")
        except ClientError as e:
            print(f"Error reading item: {e}")
            return None
        
    def create_item(self, item):
        try:
            # Check if the item already exists
            print(self.table.key_schema)
            key = {key_attr['AttributeName']: item[key_attr['AttributeName']] for key_attr in self.table.key_schema}            
            existing_item = self.read_item(key)
            if existing_item:
                print(f"Item with key {key} already exists in table {self.table.name}")
                return

            # Create the item if it does not exist
            self.table.put_item(Item=item, ConditionExpression='attribute_not_exists(PrimaryKey)')
            print(f"Item {item} created in table {self.table.name}")
        except NoCredentialsError:
            print("Credentials not available")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                print(f"Item with key {key} already exists in table {self.table.name}")
            else:
                print(f"Error creating item: {e}")
                
    def get_items_by_date_and_sort_key_prefix(self, date, sort_key_prefix):
        try:
            response = self.table.query(
                KeyConditionExpression=Key('date').eq(date) & Key('type-gameId').begins_with(sort_key_prefix)
            )
            return response.get('Items', [])
        except NoCredentialsError:
            print("Credentials not available")
            return []
        except ClientError as e:
            print(f"Error querying items: {e}")
            return []
        
    def get_items_by_date_and_exact_sort_key(self, date, sort_key):
        try:
            response = self.table.query(
                KeyConditionExpression=Key('date').eq(date) & Key('type-gameId').eq(sort_key)
            )
            return response.get('Items', [])
        except NoCredentialsError:
            print("Credentials not available")
            return []
        except ClientError as e:
            print(f"Error querying items: {e}")
            return []
    
    def get_most_recent_record(self, record_type, date):
        try:
            # scan_response = self.table.scan(
            #     FilterExpression=Attr('type-gameId').begins_with(record_type),
            #     ProjectionExpression='#d',
            #     ExpressionAttributeNames={'#d': 'date'},
            # )
            # print(record_type)
            # print('scan_response', scan_response)
            
            # if 'Items' in scan_response and len(scan_response['Items']) > 0:
            #     most_recent_date = max(item['date'] for item in scan_response['Items'])
            #     print(most_recent_date)
            # else:
            #     return None
            query_response = self.table.query(
                KeyConditionExpression=Key('date').eq(date) & Key('type-gameId').begins_with(record_type),
                ScanIndexForward=False,  # Sort in descending order by date
                Limit=1  # Get only the most recent record
            )
            
            print('query_response', query_response)
            
            if 'Items' in query_response and len(query_response['Items']) > 0:
                return query_response['Items'][0]
            else:
                return None
        except NoCredentialsError:
            print("Credentials not available")
            return None
        except ClientError as e:
            print(f"Error querying items: {e}")
            return None
    def get_all_recent_records(self, record_type, date):
        print('getting', record_type)
        try:
            most_recent_record = self.get_most_recent_record(record_type, date)
            print(most_recent_record)
            if not most_recent_record:
                return []
            
            most_recent_date = most_recent_record['date']
            
            response = self.table.query(
                KeyConditionExpression = Key('date').eq(most_recent_date) & Key('type-gameId').begins_with(record_type)
            )
            
            return response.get('Items', [])
        except NoCredentialsError:
            print("Credentials not available")
            return []
        except ClientError as e:
            print(f"Error querying items: {e}")
            return []