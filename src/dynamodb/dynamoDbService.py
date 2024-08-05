import boto3
from botocore.exceptions import NoCredentialsError, ClientError

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
