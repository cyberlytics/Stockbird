from abc import ABC
import numpy as np
import pandas as pd

import sys_src.backend.src.stockbird_logger as stockbird_logger

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
        logger.info(f'added tweets to file: {self.dest_path}')


def import_data(input_path: Path, use_cols: list, drop_cols: list, rename_cols: {}):
    """Das ist die standartmethode zum Importieren und parsen der Daten. Durch die Übergabeparameter werden die
       Datei abhängigen Attribute gesetzt, entfernt und umbenannt."""
    print(use_cols)
    if "csv" in input_path.suffix:
        data = pd.read_csv(input_path, usecols=use_cols, on_bad_lines='skip')
    elif "json" in input_path.suffix:
        data = pd.read_json(input_path, orient='split')
        data.drop(drop_cols, axis=1, inplace=True)
    else:
        raise ValueError("Input must be .csv or .json!")

    return _format_data(data, rename_cols=rename_cols)


def _format_data(data, rename_cols: {}):
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)
    data.rename(columns=rename_cols, inplace=True)
    data[TweetColumns.TIMESTAMP.value] = pd.to_datetime(data[TweetColumns.TIMESTAMP.value])
    return data


def save(data, header: bool):
    """Diese Methode fügt den übergebenen Dataframe zur Datei tweets.csv hinzu."""
    data[[TweetColumns.USERNAME.value, TweetColumns.USERFOLLOWERS.value, TweetColumns.TIMESTAMP.value,
          TweetColumns.TEXT.value, TweetColumns.RETWEETS.value, TweetColumns.USERVERIFIED.value]] \
        .to_csv(DEST_PATH / TWEETS_FILENAME, mode='a', header=header, index=False)
