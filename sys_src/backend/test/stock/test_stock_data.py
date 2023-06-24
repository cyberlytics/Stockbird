import unittest
import boto3
import json
import datetime

import botocore.errorfactory

from sys_src.backend.src.stock import stock_data

access_key_id = 'AKIATKBDO35QY726HY7J'
access_key = 'vJMAK2okWZrzv1umRgMGKqQ8FHs9NYyAjWDBhVdV'
bucket = 'stockbird-res'

s3 = boto3.client('s3',
                  aws_access_key_id=access_key_id,
                  aws_secret_access_key=access_key)


class TestStockData(unittest.TestCase):
    def setUp(self):
        # get data
        self.stock_symbol = "MSFT"
        self.file_name = f"stock_{self.stock_symbol}.json"

        # is updated
        self.outdated_symbol = "APPL.DE"
        self.outdated_file_name = f"stock_{self.outdated_symbol}.json"

        # filter by date
        self.start_date = "2020-01-02"
        self.end_date = "2022-04-04"

        self.dt_start_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d").date()
        self.dt_end_date = datetime.datetime.strptime(self.end_date, "%Y-%m-%d").date()

    def test_get_data(self):
        stock_data.query_stocks(self.stock_symbol, self.file_name)
        response = s3.get_object(Bucket=bucket, Key=self.file_name)
        json_data = json.loads(response['Body'].read().decode('utf-8'))
        self.assertIsNotNone(json_data)

    def test_is_data_updated(self):
        stock_data.query_stocks(self.stock_symbol, self.file_name)
        self.assertTrue(stock_data._is_data_updated(self.file_name))
        self.assertFalse(stock_data._is_data_updated(self.outdated_file_name))

    def test_filter_by_date(self):
        data = stock_data.query_stocks(self.stock_symbol, self.file_name)
        filtered_df = stock_data.query_stock_by_date(data, self.start_date, self.end_date)

        self.assertEqual(filtered_df.index[0], self.dt_start_date)
        self.assertEqual(filtered_df.index[-1], self.dt_end_date)
