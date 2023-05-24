import sys
import pandas as pd
import numpy as np
from pathlib import Path
backend_path = Path(__file__).absolute().parent.parent.parent
sys.path.append(str(backend_path))
from Constants import TweetColumns



def _importData(file_path: Path, format_type: str):
    if format_type == 'csv':
        return pd.read_csv(file_path, on_bad_lines='skip')
    # Todo: add import for different file formats


class ParserTwo:

    def __init__(self, file_path: Path, format_type: str = 'csv'):
        self.res_path = backend_path / 'res'
        self.data = _importData(file_path, format_type)
        self.file_path = file_path
        self.format_type = format_type

        self._removeUnusedColumns(['id', 'url', 'company_names', 'symbols'])
        self._renameColumns({'verified': TweetColumns.USERVERIFIED.value,
                             'source': TweetColumns.USERNAME.value})
        self._addMissingColumns([TweetColumns.RETWEETS.value, TweetColumns.USERFOLLOWERS.value])
        self._changeTimestampFormat()

    def _removeUnusedColumns(self, column_names: list):
        for i in column_names:
            self.data.pop(i)

    def _renameColumns(self, column_names: dict):
        self.data.rename(columns=column_names, inplace=True)

    def _addMissingColumns(self, missing_columns: list):
        for i in missing_columns:
            self.data[i] = np.nan

    def _changeTimestampFormat(self, time_format: str = '%a %b %d %H:%M:%S %z %Y'):
        self.data[TweetColumns.TIMESTAMP.value] = \
            pd.to_datetime(self.data[TweetColumns.TIMESTAMP.value], format=time_format)

    def appendToFile(self, file_path: Path):
        self.data.to_csv(file_path, mode='a', index=False)
