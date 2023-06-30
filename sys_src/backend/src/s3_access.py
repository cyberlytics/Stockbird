import json
import boto3
import stockbird_logger

import pandas as pd

from sys_src.backend.src.Constants import *

logger = stockbird_logger.get_logger(LOGGER_NAME)

s3 = boto3.client('s3',
                  aws_access_key_id=ACCESS_KEY_ID,
                  aws_secret_access_key=ACCESS_KEY)


def read_json(file_name):
    response = s3.get_object(Bucket=BUCKET, Key=file_name)
    json_data = json.loads(response['Body'].read().decode('utf-8'))
    logger.info(f'File: {file_name}')
    return json_data


def write_json(json_data, file_name):
    json_str = json.dumps(json_data)
    s3.put_object(Body=json_str, Bucket=BUCKET, Key=file_name)
    logger.info(f'"{json_data}" converted to string in "{file_name}"')


def write_log(log_data, file_name):
    s3.put_object(Body=log_data, Bucket=BUCKET, Key=file_name)


def get_all_logs():
    files = [sub['Key'] for sub in s3.list_objects(Bucket=BUCKET)['Contents'] if '.log' in sub['Key']]
    logger.info('All saved logs:')
    return sorted(files, key=lambda x: datetime.datetime.strptime(x, 'stockbird-%Y-%m-%d.log'))


def try_remove_oldest_log():
    if len(get_all_logs()) >= 30 and not exists_log_for_today():
        s3.delete_object(Bucket=BUCKET, Key=get_all_logs()[0])
        logger.info('Oldest log deleted')


def exists_log_for_today():
    if f'stockbird-{datetime.date.today().strftime("%Y-%m-%d")}.log' in get_all_logs():
        logger.info("There are logs available for today")
    else:
        logger.info("There are no logs available for today")
    return f'stockbird-{datetime.date.today().strftime("%Y-%m-%d")}.log' in get_all_logs()


def read_log(file_name):
    response = s3.get_object(Bucket=BUCKET, Key=file_name)
    logger.info(f'Contens of the "{file_name}" logger')
    return response['Body'].read().decode('utf-8')


def update_log(log_data, file_name):
    data = read_log(file_name)
    data += log_data
    write_log(data, file_name)
    logger.info(f'"{file_name}" log updated')


def update_json(file_name, updated_data):
    data = read_json(file_name)
    data.update(updated_data)
    write_json(data, file_name)
    logger.info(f'"{file_name}" updated')


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
    response = s3.get_object(Bucket=BUCKET, Key=file_name)
    csv_data = pd.read_csv(response['Body'])
    csv_data[TweetColumns.TIMESTAMP.value] = pd.to_datetime(csv_data[TweetColumns.TIMESTAMP.value])
    logger.info(f'"{file_name}" has been read timestamped and converted to panda')
    return csv_data


# Read CSV data from a file in S3
def read_csv_for_stock_captions(file_name):
    response = s3.get_object(Bucket=BUCKET, Key=file_name)
    csv_data = pd.read_csv(response['Body'])
    logger.info(f'"{file_name}" has been read and converted to panda')
    return csv_data


"""
file_name = 'example.csv'

retrieved_data = read_csv(file_key)
print('Retrieved CSV data from S3:')
print(retrieved_data)
"""


def write_csv(data, file_name):
    # append data to an existed csv-file on the S3 bucket and save it.
    current_data = pd.DataFrame()

    files = [sub['Key'] for sub in s3.list_objects(Bucket=BUCKET)['Contents'] if '.csv' in sub['Key']]
    if file_name in files:
        current_data = pd.read_csv(s3.get_object(Bucket=BUCKET, Key=file_name)['Body'])

    appended_data_encode = pd.concat([current_data, data], ignore_index=True) \
        .to_csv(None, index=False, header=True if file_name in files else False) \
        .encode('utf-8')
    if file_name in files:
        logger.info(f'"{data}" has been added to "{file_name}"')
    else:
        logger.info(f'"{file_name}" has been created')
    s3.put_object(Body=appended_data_encode, Bucket=BUCKET, Key=file_name)
