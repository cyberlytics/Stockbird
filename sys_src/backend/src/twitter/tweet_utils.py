import sys_src.backend.src.s3_access as s3
import pandas as pd
import sys_src.backend.src.stockbird_logger as stockbird_logger

from sys_src.backend.src.Constants import *

logger = stockbird_logger.get_logger(LOGGER_NAME)


def query_tweets_by_stock_name(tweets_file_name: str, stock_name: str):
    """try to find every tweet containing the stockname in its text"""
    df = s3.read_csv(tweets_file_name)
    df = _query_tweets_by_substring(df, TweetColumns.TEXT, stock_name)
    return df.to_json(orient='split', index=False, indent=4)


def _query_tweets_by_substring(df: pd.DataFrame, column: TweetColumns, sub_string: str = None):
    if not sub_string:
        logger.info(f'sub_string is empty whole dataframe will be returned')
        return df

    df = df[df[column.value].str.contains(sub_string)]
    logger.info(f'filtered tweets by column {TweetColumns.TEXT} containing {sub_string}')
    return df


def _query_tweets_by_date(df: pd.DataFrame, date_from: datetime = None, date_to: datetime = None):
    logger.info(f'filtered dataframe by date from {date_from} to {date_to}')
    test_df = df[df[TweetColumns.TIMESTAMP] > date_from] if date_from is not None else df
    return test_df[test_df[TweetColumns.TIMESTAMP < date_from]] if date_to is not None else test_df
