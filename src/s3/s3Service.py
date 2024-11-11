from io import StringIO
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import pandas as pd

class S3Service:
    def __init__(self, bucketName):
        self.s3_client = boto3.client('s3')
        self.bucketName=bucketName
        
    def list_files(self, bucket_name):
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                return [item['Key'] for item in response['Contents']]
            else:
                return []
        except ClientError as e:
            print(f"Error listing files: {e}")
            return []

    def download_file(self, bucket_name, s3_key, local_path):
        try:
            self.s3_client.download_file(bucket_name, s3_key, local_path)
            print(f"File {s3_key} downloaded to {local_path}")
        except NoCredentialsError:
            print("Credentials not available")
        except ClientError as e:
            print(f"Error downloading file: {e}")

    def get_schedule(self):
        s3_key = 'NBA_Schedule_2024_25.csv'
        local_path = '/tmp/'


        # self.download_file(self.bucketName, s3_key, local_path)
        csv_obj = self.s3_client.get_object(Bucket=self.bucketName, Key=s3_key)
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')

        df = pd.read_csv(StringIO(csv_string))

        return df

# Example event for testing
# event = {
#     'bucket_name': 'your_bucket_name',
#     's3_key': 'your_s3_key'
# }
# context = {}
# print(lambda_handler(event, context))