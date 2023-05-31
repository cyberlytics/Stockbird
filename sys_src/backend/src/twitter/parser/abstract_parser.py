from abc import ABC
from pathlib import Path

import numpy as np
import pandas as pd

from sys_src.backend.Constants import TweetColumns, DEST_PATH, TWEETS_FILENAME


class AbstractParser(ABC):

    def __init__(self, source_path: Path):
        self.source_path = source_path
        self.dest_path = DEST_PATH / TWEETS_FILENAME
        self.format_type = source_path.suffix
        self.data = self._import_data()

    def _import_data(self):
        if self.format_type == '.csv':
            return pd.read_csv(self.source_path, on_bad_lines='skip')
        if self.format_type == '.json':
            return pd.read_json(self.source_path, orient='split')

    def _remove_unused_columns(self, column_names: list):
        for i in column_names:
            self.data.pop(i)

    def _rename_columns(self, column_names: dict):
        self.data.rename(columns=column_names, inplace=True)

    def _add_missing_columns(self, missing_columns: list):
        for i in missing_columns:
            self.data[i] = np.nan

    def _change_timestamp_format(self, time_format: str = None):
        self.data[TweetColumns.TIMESTAMP.value] = \
            pd.to_datetime(self.data[TweetColumns.TIMESTAMP.value], format=time_format)

    def _change_column_order(self, column_list: list):
        self.data = self.data.loc[:, column_list]

    def append_to_file(self):
        self.data.to_csv(self.dest_path, mode='a', index=False,
                         header=False if self.dest_path.is_file() else True)


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
          TweetColumns.TEXT.value, TweetColumns.RETWEETS.value, TweetColumns.USERVERIFIED.value]]\
        .to_csv(DEST_PATH / TWEETS_FILENAME, mode='a', header=header, index=False)
