import os

import pandas as pd

from sys_src.backend.src.twitter.parser import parser_three
from pathlib import Path


INPUT_PATH = Path(__file__).absolute().parent.parent / 'data/input'
OUTPUT_PATH = Path(__file__).absolute().parent.parent / 'data/output'


def test_import_data():
    _remove_file(OUTPUT_PATH / 'parser_three_test_data.csv')
    parser_three._import_data(input_path=INPUT_PATH / 'parser_three_test_data.csv',
                              user_name='TEST_USER',
                              user_verified=True,
                              user_follower=888950,
                              dest_path=OUTPUT_PATH / 'parser_three_test_data.csv')

    _assert_data_frames(OUTPUT_PATH / 'parser_three_test_data.csv',
                        OUTPUT_PATH / 'parser_three_test_control_data.csv')
    _remove_file(OUTPUT_PATH / 'parser_three_test_data.csv')


def test_import_no_args_data():
    _remove_file(OUTPUT_PATH / 'parser_three_test_no_args_data.csv')
    parser_three._import_data(input_path=INPUT_PATH / 'parser_three_test_data.csv',
                              dest_path=OUTPUT_PATH / 'parser_three_test_no_args_data.csv')

    _assert_data_frames(OUTPUT_PATH / 'parser_three_test_no_args_data.csv',
                        OUTPUT_PATH / 'parser_three_test_no_args_control_data.csv')
    _remove_file(OUTPUT_PATH / 'parser_three_test_no_args_data.csv')


def _assert_data_frames(to_check, control):
    data_to_check = pd.read_csv(to_check, on_bad_lines='skip')
    control_data = pd.read_csv(control, on_bad_lines='skip')

    pd.testing.assert_frame_equal(data_to_check, control_data)


def _remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
