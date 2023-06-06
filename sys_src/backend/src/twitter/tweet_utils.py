import backend.src.s3_access as s3
import pandas as pd
import datetime
import os
import sys_src.backend.src.StockbirdLogger as StockbirdLogger
from sys_src.backend.Constants import *

logger = StockbirdLogger.get_logger(LOGGER_NAME)


def query_tweets_by_stockname(tweets_file_name: str, stock_name: str):
    """try to find every tweet containing the stockname in its text"""
    df = get_tweets_from_csv(s3.read_csv(tweets_file_name))
    df = _query_tweets_by_substring(df, stock_name, TweetColumns.TEXT)
    create_json(df, DEST_PATH / 'tweets_by_stockname.json')


def _query_tweets_by_substring(df: pd.DataFrame, sub_string: str, column: TweetColumns):
    if not sub_string:
        logger.error(f'sub_string is empty whole dataframe will be returned')
        return df

    df = df[df[column.value].str.contains(sub_string)]
    logger.info(f'filtered tweets by column {TweetColumns.TEXT} containing {sub_string}')
    return df


def _query_tweets_by_date(df: pd.DataFrame, date_from: datetime = None, date_to: datetime = None):
    if not date_from and not date_to:
        logger.warning(f'No date passed, whole dataframe (all tweets) will be returned!')
        return df
    elif not date_from:
        logger.info(f'filter tweets from begin until {date_to}')
        return df[df[TweetColumns.TIMESTAMP] < date_to]
    elif not date_to:
        logger.info(f'filter tweets from {date_from} until end')
        return df[df[TweetColumns.TIMESTAMP] > date_from]


def try_remove_file(dest_file: Path):
    """wrapper method to remove files with logging"""
    if os.path.exists(dest_file):
        os.remove(dest_file)
        logger.info(f'removed file {dest_file} cause of new request')
    else:
        logger.info(f'file or directory not found {dest_file}')


def exists_file(file: Path):
    """wrapper method to check if a file exists with logging"""
    if not os.path.exists(file):
        logger.error(f'file or directory not found {file}')
        return False
    return True


def is_file_empty(file: Path):
    """wrapper method to check whether a file is empty with logging"""
    if os.stat("file").st_size == 0:
        logger.warning(f'file is empty {file}')
        return True
    return False


def create_json(df: pd.DataFrame, dest_file: Path):
    try_remove_file(dest_file)
    df.to_json(dest_file, orient='split', index=False, indent=4)
    logger.info(f'created file {dest_file} cause of new request')


def get_tweets_from_csv(tweets_file_path: Path):
    if exists_file(tweets_file_path) or not is_file_empty(tweets_file_path):
        return pd.read_csv(tweets_file_path)
    raise FileNotFoundError(f'File does not exist or is empty')