import json
import os
from pathlib import Path
from sys_src.backend.src.analysation import twitter_analysis

import pandas as pd

INPUT_PATH = Path(__file__).absolute().parent.parent / 'data/input'
OUTPUT_PATH = Path(__file__).absolute().parent.parent / 'data/output'


def test_query_relevant_tweets_by_stock_filter():
    input_data = pd.read_csv(INPUT_PATH / 'twitter_analysis_test.csv', on_bad_lines='skip')
    result = json.loads(twitter_analysis.query_relevant_tweets_by_stock(input_data, 'TSLA', ''))

    result = pd.DataFrame(result['data'], columns=result['columns'])
    control_data = pd.read_csv(OUTPUT_PATH / 'twitter_analysis_test_stock_filter.csv', on_bad_lines='skip')

    assert len(result) == 4
    pd.testing.assert_frame_equal(result, control_data)


def test_query_relevant_tweets_by_stock_no_filter():
    input_data = pd.read_csv(INPUT_PATH / 'twitter_analysis_test.csv', on_bad_lines='skip')
    result = json.loads(twitter_analysis.query_relevant_tweets_by_stock(input_data, 'TSLA', 'socks'))

    result = pd.DataFrame(result['data'], columns=result['columns'])
    control_data = pd.read_csv(OUTPUT_PATH / 'twitter_analysis_test_stock_no_filter.csv', on_bad_lines='skip')

    assert len(result) == 5
    pd.testing.assert_frame_equal(result, control_data)


def test_query_relevant_tweets_by_stock_no_filter_two_substrings():
    input_data = pd.read_csv(INPUT_PATH / 'twitter_analysis_test.csv', on_bad_lines='skip')
    result = json.loads(twitter_analysis.query_relevant_tweets_by_stock(input_data, 'TSLA', 'socks, Always'))

    result = pd.DataFrame(result['data'], columns=result['columns'])
    control_data = pd.read_csv(OUTPUT_PATH / 'twitter_analysis_test_stock_no_filter_two_substrings.csv', on_bad_lines='skip')

    assert len(result) == 5
    pd.testing.assert_frame_equal(result, control_data)
