import os

import pandas as pd

from src.twitter.parser import parser_one
from pathlib import Path


INPUT_PATH = Path(__file__).absolute().parent.parent / 'data/input'
OUTPUT_PATH = Path(__file__).absolute().parent.parent / 'data/output'


def test_import_data():
    _remove_file(OUTPUT_PATH / 'parser_one_test_data.csv')
    parser_one._import_data(INPUT_PATH / 'parser_one_test_data.csv', OUTPUT_PATH / 'parser_one_test_data.csv')

    data_to_check = pd.read_csv(OUTPUT_PATH / 'parser_one_test_data.csv', on_bad_lines='skip')
    control_data = pd.read_csv(OUTPUT_PATH / 'parser_one_test_control_data.csv', on_bad_lines='skip')
    pd.testing.assert_frame_equal(data_to_check, control_data)
    _remove_file(OUTPUT_PATH / 'parser_one_test_data.csv')


def _remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
