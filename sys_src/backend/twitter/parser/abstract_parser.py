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
