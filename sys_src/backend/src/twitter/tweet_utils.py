import sys_src.backend.src.s3_access as s3
import pandas as pd
import sys_src.backend.src.stockbird_logger as stockbird_logger
from datetime import datetime
from sys_src.backend.src.Constants import *

logger = stockbird_logger.get_logger(LOGGER_NAME)


def query_tweets_by_stock(tweets_file_name: str, date_from, date_to, substrings: str):
    return _query_tweets_by_stock(tweets_file_name, date_from, date_to, substrings)\
        .to_json(orient='split', index=False, indent=4)


def query_tweets(tweets_file_name: str, date_from, date_to):
    df = s3.read_csv(tweets_file_name)
    df = _query_tweets_by_date(df,
                               datetime.datetime.strptime(date_from, FRONTEND_DATE_FORMAT)
                               .replace(tzinfo=datetime.timezone.utc) if date_from is not None else None,
                               datetime.datetime.strptime(date_to, FRONTEND_DATE_FORMAT)
                               .replace(tzinfo=datetime.timezone.utc) if date_to is not None else None)
    return df.to_json(orient='split', index=False, indent=4)


def query_relevant_tweets_by_stock(tweets_file_name: str, date_from, date_to, substrings: str):
    return _query_tweets_by_stock(tweets_file_name, date_from, date_to, substrings)


def _query_tweets_by_stock(tweets_file_name: str, date_from, date_to, substrings: str):
    df = s3.read_csv(tweets_file_name)
    result_df = pd.DataFrame(data=None, columns=df.columns)
    for stock_name in substrings.split(','):
        result_df = pd.concat([result_df, _query_tweets_by_substring(df, TweetColumns.TEXT, stock_name)])
    return _query_tweets_by_date(result_df,
                                 datetime.datetime.strptime(date_from, FRONTEND_DATE_FORMAT)
                                 .replace(tzinfo=datetime.timezone.utc) if date_from is not None else None,
                                 datetime.datetime.strptime(date_to, FRONTEND_DATE_FORMAT)
                                 .replace(tzinfo=datetime.timezone.utc) if date_to is not None else None)


def _query_tweets_by_substring(df: pd.DataFrame, column: TweetColumns, sub_string: str):
    """Returns all entries of a Dataframe that contain the substring in the defined column"""
    if not sub_string:
        logger.info(f'sub_string is empty whole dataframe will be returned')
        return df

    df = df[df[column.value].str.contains(sub_string)]
    logger.info(f'filtered tweets by column {TweetColumns.TEXT.value} containing {sub_string}')
    return df


def _query_tweets_by_date(df: pd.DataFrame, date_from: datetime = None, date_to: datetime = None):
    """Returns all entries from a Dataframe that are in the time span. In case no time span
    is overgiven the whole Dataframe will be returned"""
    logger.info(f'filtered dataframe by date from {date_from} to {date_to}')
    df = df[df[TweetColumns.TIMESTAMP.value] >= date_from] if date_from is not None else df
    return df[df[TweetColumns.TIMESTAMP.value] <= date_to] if date_to is not None else df
