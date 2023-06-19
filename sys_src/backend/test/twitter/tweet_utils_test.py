import pandas as pd
import sys_src.backend.src.twitter.tweet_utils as tweet_utils
from sys_src.backend.src.Constants import *

INPUT_PATH = Path(__file__).absolute().parent.parent / 'data' / 'input'
OUTPUT_PATH = Path(__file__).absolute().parent.parent / 'data' / 'output' / 'tweet_utils'


def test_query_tweets_by_date_from_and_to():
    input_df = _read_test_data(INPUT_PATH / 'abstract_parser_test_data.csv')
    input_df[TweetColumns.TIMESTAMP.value] = pd.to_datetime(input_df[TweetColumns.TIMESTAMP.value])
    date_from = datetime.datetime.strptime('05.07.2022 14:00:21+00:00', '%d.%m.%Y %H:%M:%S%z')
    date_to = datetime.datetime.strptime('05.07.2022 17:55:09+00:00', '%d.%m.%Y %H:%M:%S%z')

    result_df = tweet_utils._query_tweets_by_date(input_df, date_from, date_to)
    pd.testing.assert_frame_equal(_read_test_data(OUTPUT_PATH / 'query_tweets_by_date_from_and_to.csv'),
                                  result_df.reset_index(drop=True))


def test_query_tweets_by_date_from():
    input_df = _read_test_data(INPUT_PATH / 'abstract_parser_test_data.csv')
    input_df[TweetColumns.TIMESTAMP.value] = pd.to_datetime(input_df[TweetColumns.TIMESTAMP.value])
    date_from = datetime.datetime.strptime('2022-07-05 17:47:42+00:00', '%Y-%m-%d %H:%M:%S%z')

    result_df = tweet_utils._query_tweets_by_date(input_df, date_from, None)
    pd.testing.assert_frame_equal(_read_test_data(OUTPUT_PATH / 'query_tweets_by_date_from.csv'),
                                  result_df.reset_index(drop=True))


def test_query_tweets_by_date_to():
    input_df = _read_test_data(INPUT_PATH / 'abstract_parser_test_data.csv')
    input_df[TweetColumns.TIMESTAMP.value] = pd.to_datetime(input_df[TweetColumns.TIMESTAMP.value])
    date_to = datetime.datetime.strptime('2022-07-05 17:36:03+00:00', '%Y-%m-%d %H:%M:%S%z')

    result_df = tweet_utils._query_tweets_by_date(input_df, None, date_to)
    pd.testing.assert_frame_equal(_read_test_data(OUTPUT_PATH / 'query_tweets_by_date_to.csv'),
                                  result_df.reset_index(drop=True))


def test_query_tweets_by_date_none_none():
    input_df = _read_test_data(INPUT_PATH / 'abstract_parser_test_data.csv')
    input_df[TweetColumns.TIMESTAMP.value] = pd.to_datetime(input_df[TweetColumns.TIMESTAMP.value])

    result_df = tweet_utils._query_tweets_by_date(input_df, None, None)
    pd.testing.assert_frame_equal(_read_test_data(INPUT_PATH / 'abstract_parser_test_data.csv'),
                                  result_df.reset_index(drop=True))


def test_query_tweets_by_substring():
    input_df = _read_test_data(INPUT_PATH / 'abstract_parser_test_data.csv')
    input_df[TweetColumns.TIMESTAMP.value] = pd.to_datetime(input_df[TweetColumns.TIMESTAMP.value])

    result_df = tweet_utils._query_tweets_by_substring(input_df, TweetColumns.TEXT, "for")
    pd.testing.assert_frame_equal(_read_test_data(OUTPUT_PATH / 'query_tweets_by_substring.csv'),
                                  result_df.reset_index(drop=True))


def _read_test_data(file_path: Path):
    df = pd.read_csv(file_path)
    df[TweetColumns.TIMESTAMP.value] = pd.to_datetime(df[TweetColumns.TIMESTAMP.value])
    return df
