import unittest
import boto3
import json
import datetime

import pandas as pd

from sys_src.backend.src.stock import stock_analysis
from sys_src.backend.src.stock import stock_data

access_key_id = 'AKIATKBDO35QY726HY7J'
access_key = 'vJMAK2okWZrzv1umRgMGKqQ8FHs9NYyAjWDBhVdV'
bucket = 'stockbird-res'

s3 = boto3.client('s3',
                  aws_access_key_id=access_key_id,
                  aws_secret_access_key=access_key)

class TestStockAnalysis(unittest.TestCase):
    def setUp(self):
        # get data
        self.stock_symbol = "MSFT"
        self.file_name = f"stock_{self.stock_symbol}.json"
        self.df_msft = stock_data.query_stocks(self.stock_symbol, self.file_name)

        # empty file
        self.empty_data = ""


    def test_query_peak_from_stock(self):
        # function returns a json as string
        json_peaks = stock_analysis.query_peaks_from_stock(str_data=self.df_msft, days=7, percent=5.0)
        # for testing output, you need a list to check amount of results
        list_peaks = json.loads(json_peaks)
        # this one should have entries
        self.assertGreater(len(list_peaks), 0)

        # testing with more than 100%, should be empty list
        json_peaks = stock_analysis.query_peaks_from_stock(str_data=self.df_msft, days=7, percent=105.0)
        list_peaks = json.loads(json_peaks)
        # this one should have entries
        self.assertEqual(len(list_peaks), 0)

        # testing with less then one day, should be empty list
        json_peaks = stock_analysis.query_peaks_from_stock(str_data=self.df_msft, days=-2, percent=5.0)
        list_peaks = json.loads(json_peaks)
        # this one should have entries
        self.assertEqual(len(list_peaks), 0)

        # testing with empty data, should be empty list
        json_peaks = stock_analysis.query_peaks_from_stock(str_data=self.empty_data, days=7, percent=5.0)
        list_peaks = json.loads(json_peaks)
        # this one should have entries
        self.assertEqual(len(list_peaks), 0)
