import numpy as np
import pandas as pd

import sys_src.backend.src.s3_access as s3_bucket
import sys_src.backend.src.stockbird_logger as stockbird_logger

from abc import ABC
from sys_src.backend.src.Constants import *

logger = stockbird_logger.get_logger(LOGGER_NAME)


class AbstractParser(ABC):

    def __init__(self, source_path: Path):
        self.source_path: Path = source_path
        self.dest_path: Path = DEST_PATH / TWEETS_FILENAME
        self.format_type: str = source_path.suffix
        self.data: pd.DataFrame = self._import_data()

    def _import_data(self):
        if self.format_type == '.csv':
            return pd.read_csv(self.source_path, on_bad_lines='skip')
        if self.format_type == '.json':
            return pd.read_json(self.source_path, orient='split')

    def _remove_unused_columns(self, column_names: list):
        logger.info(f'removed following columns {column_names}')
        for i in column_names:
            self.data.pop(i)

    def _rename_columns(self, column_names: dict):
        self.data.rename(columns=column_names, inplace=True)
        logger.info(f'renamed following columns {column_names}')

    def _add_missing_columns(self, missing_columns: list):
        for i in missing_columns:
            self.data[i] = np.nan
        logger.info(f'added missing columns {missing_columns}')

    def _change_timestamp_format(self, time_format: str = None):
        self.data[TweetColumns.TIMESTAMP.value] = \
            pd.to_datetime(self.data[TweetColumns.TIMESTAMP.value], format=time_format)
        logger.info(f'changed timestamp format to default datetime format')

    def _change_column_order(self, column_list: list):
        self.data = self.data.loc[:, column_list]
        logger.info(f'changed column order from [ {self.data.columns} to {column_list} ]')

    def append_to_file(self):
        """add tweets to a given file if file does not exist it will be created"""
        self.data.to_csv(self.dest_path, mode='a', index=False,
                         header=False if self.dest_path.is_file() else True)
        s3_bucket.write_csv(self.data, file_name=TWEETS_FILENAME, header=False if self.dest_path.is_file() else True)
        logger.info(f'added tweets to file: {self.dest_path}')


def import_data(input_path: Path, use_cols: list, drop_cols: list, rename_cols: {}):
    """Das ist die standartmethode zum Importieren und parsen der Daten. Durch die Übergabeparameter werden die
       Datei abhängigen Attribute gesetzt, entfernt und umbenannt."""
    if "csv" in input_path.suffix:
        data = pd.read_csv(input_path, usecols=use_cols, on_bad_lines='skip')
    elif "json" in input_path.suffix:
        data = pd.read_json(input_path, orient='split')
        data.drop(drop_cols, axis=1, inplace=True)
    else:
        logger.info(f'The given File {input_path} is no .csv or .json file-format.')
        raise ValueError("Input must be .csv or .json!")

    logger.info(f'The import of the given File {input_path} was successful.')
    return _format_data(data, rename_cols=rename_cols)


def _format_data(data, rename_cols: {}):
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)
    data.rename(columns=rename_cols, inplace=True)
    data[TweetColumns.TIMESTAMP.value] = pd.to_datetime(data[TweetColumns.TIMESTAMP.value], utc=True)
    return data


def save(data, header: bool = False, dest_path=None):
    """Diese Methode fügt den übergebenen Dataframe zur Datei tweets.csv hinzu."""
    data = data[[TweetColumns.USERNAME.value, TweetColumns.USERFOLLOWERS.value, TweetColumns.TIMESTAMP.value,
                 TweetColumns.TEXT.value, TweetColumns.RETWEETS.value, TweetColumns.USERVERIFIED.value]]
    if dest_path is None:
        # add data to data on S3 bucket.
        s3_bucket.write_csv(data, file_name=TWEETS_FILENAME, header=header)
        logger.info(f'added tweets to file on S3 bucket: {TWEETS_FILENAME}')
    else:
        # add data to specific destination, mainly for testing.
        data.to_csv(dest_path, mode='a', header=header, index=False)
        logger.info(f'added tweets to file: {dest_path}')
