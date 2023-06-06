import json
import boto3
import pandas as pd

access_key_id = 'AKIATKBDO35QY726HY7J'
access_key = 'vJMAK2okWZrzv1umRgMGKqQ8FHs9NYyAjWDBhVdV'
bucket = 'stockbird-res'


s3 = boto3.client('s3',
                  aws_access_key_id=access_key_id,
                  aws_secret_access_key=access_key)

def read_json(file_name):
    response = s3.get_object(Bucket=bucket, Key=file_name)
    json_data = json.loads(response['Body'].read().decode('utf-8'))
    return json_data

def write_json(json_data, file_name):
    json_str = json.dumps(json_data)
    s3.put_object(Body=json_str, Bucket=bucket, Key=file_name)

def update_json(file_name, updated_data):
    data = read_json(file_name)
    data.update(updated_data)
    write_json(data, file_name)


"""
data = {
    'name': 'Bob',
    'age': 20,
    'city': 'Magstadt'
}

file_name = 'example.json'

write_json(data, file_key)

retrieved_data = read_json(file_key)
print('Retrieved JSON data from S3:', retrieved_data)

update_data = {'age': 31, 'city': 'San Francisco'}
update_json(file_key, update_data)

updated_data = read_json(file_key)
print('Updated JSON data:', updated_data)
"""

# Read CSV data from a file in S3
def read_csv(file_name):
    response = s3.get_object(Bucket=bucket, Key=file_name)
    csv_data = pd.read_csv(response['Body'])
    return csv_data

"""
file_name = 'example.csv'

retrieved_data = read_csv(file_key)
print('Retrieved CSV data from S3:')
print(retrieved_data)
"""