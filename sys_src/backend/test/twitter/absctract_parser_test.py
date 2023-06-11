import os

import pandas as pd
import sys_src.backend.src.twitter.parser.abstract_parser as ap

from pathlib import Path
from sys_src.backend.src.Constants import TweetColumns

INPUT_PATH = Path(__file__).absolute().parent.parent / 'data/input'
OUTPUT_PATH = Path(__file__).absolute().parent.parent / 'data/output'


def test_import_data():
    _remove_file(OUTPUT_PATH / 'abstract_parser_import_test_data.csv')
    import_data = ap.import_data(input_path=INPUT_PATH / 'abstract_parser_test_data.csv',
                                 use_cols=[TweetColumns.USERNAME.value, TweetColumns.USERFOLLOWERS.value,
                                           TweetColumns.TIMESTAMP.value, TweetColumns.TEXT.value,
                                           TweetColumns.RETWEETS.value, TweetColumns.USERVERIFIED.value],
                                 drop_cols=[],
                                 rename_cols={})
    import_data.to_csv(OUTPUT_PATH / 'abstract_parser_import_test_data.csv', header=True, index=False)

    _assert_data_frames(OUTPUT_PATH / 'abstract_parser_import_test_data.csv',
                        OUTPUT_PATH / 'abstract_parser_import_test_control_data.csv')
    _remove_file(OUTPUT_PATH / 'abstract_parser_import_test_data.csv')


def test_import_data_rename_column():
    _remove_file(OUTPUT_PATH / 'abstract_parser_rename_test_data.csv')
    import_data = ap.import_data(input_path=INPUT_PATH / 'abstract_parser_test_data.csv',
                                 use_cols=[TweetColumns.USERNAME.value, TweetColumns.USERFOLLOWERS.value,
                                           TweetColumns.TIMESTAMP.value, TweetColumns.TEXT.value,
                                           TweetColumns.RETWEETS.value, TweetColumns.USERVERIFIED.value],
                                 drop_cols=[],
                                 rename_cols={TweetColumns.RETWEETS.value: 'Rename1',
                                              TweetColumns.USERVERIFIED.value: 'Rename2'})
    import_data.to_csv(OUTPUT_PATH / 'abstract_parser_rename_test_data.csv', header=True, index=False)

    _assert_data_frames(OUTPUT_PATH / 'abstract_parser_rename_test_data.csv',
                        OUTPUT_PATH / 'abstract_parser_rename_test_control_data.csv')
    _remove_file(OUTPUT_PATH / 'abstract_parser_rename_test_data.csv')


def test_import_data_json():
    _remove_file(OUTPUT_PATH / 'abstract_parser_import_test_data_json.csv')
    import_data = ap.import_data(input_path=INPUT_PATH / 'abstract_parser_test_data.json',
                                 use_cols=[],
                                 drop_cols=[],
                                 rename_cols={})
    import_data.to_csv(OUTPUT_PATH / 'abstract_parser_import_test_data_json.csv', header=True, index=False)

    _assert_data_frames(OUTPUT_PATH / 'abstract_parser_import_test_data_json.csv',
                        OUTPUT_PATH / 'abstract_parser_import_test_data_json.csv')
    _remove_file(OUTPUT_PATH / 'abstract_parser_import_test_data_json.csv')


def test_import_data_rename_column_json():
    _remove_file(OUTPUT_PATH / 'abstract_parser_rename_test_data_json.csv')
    import_data = ap.import_data(input_path=INPUT_PATH / 'abstract_parser_test_data.json',
                                 use_cols=[],
                                 drop_cols=[],
                                 rename_cols={TweetColumns.RETWEETS.value: 'Rename1',
                                              TweetColumns.USERVERIFIED.value: 'Rename2'})
    import_data.to_csv(OUTPUT_PATH / 'abstract_parser_rename_test_data_json.csv', header=True, index=False)

    _assert_data_frames(OUTPUT_PATH / 'abstract_parser_rename_test_data_json.csv',
                        OUTPUT_PATH / 'abstract_parser_rename_test_control_data.csv')
    _remove_file(OUTPUT_PATH / 'abstract_parser_rename_test_data_json.csv')


def test_import_data_drop_columns():
    _remove_file(OUTPUT_PATH / 'abstract_parser_drop_test_data_json.csv')

    import_data = ap.import_data(input_path=INPUT_PATH / 'abstract_parser_test_data.json',
                                 use_cols=[TweetColumns.USERNAME.value, TweetColumns.USERFOLLOWERS.value,
                                           TweetColumns.TIMESTAMP.value, TweetColumns.TEXT.value,
                                           TweetColumns.RETWEETS.value, TweetColumns.USERVERIFIED.value],
                                 drop_cols=[TweetColumns.USERVERIFIED.value],
                                 rename_cols={})
    import_data.to_csv(OUTPUT_PATH / 'abstract_parser_drop_test_data_json.csv', header=True, index=False)

    _assert_data_frames(OUTPUT_PATH / 'abstract_parser_drop_test_data_json.csv',
                        OUTPUT_PATH / 'abstract_parser_drop_test_control_data.csv')
    _remove_file(OUTPUT_PATH / 'abstract_parser_drop_test_data_json.csv')


def test_save_data():
    _remove_file(OUTPUT_PATH / 'abstract_parser_save_test_data.csv')

    save_data = pd.read_csv(INPUT_PATH / 'abstract_parser_test_data.csv')
    ap.save(save_data, header=True, dest_path=OUTPUT_PATH / 'abstract_parser_save_test_data.csv')

    _assert_data_frames(OUTPUT_PATH / 'abstract_parser_save_test_data.csv',
                        OUTPUT_PATH / 'abstract_parser_import_test_control_data.csv')
    _remove_file(OUTPUT_PATH / 'abstract_parser_save_test_data.csv')


def test_save_data_append():
    _remove_file(OUTPUT_PATH / 'abstract_parser_save_test_data.csv')

    save_data = pd.read_csv(INPUT_PATH / 'abstract_parser_test_data.csv')
    ap.save(save_data, header=True, dest_path=OUTPUT_PATH / 'abstract_parser_save_test_data.csv')
    ap.save(save_data, header=False, dest_path=OUTPUT_PATH / 'abstract_parser_save_test_data.csv')

    _assert_data_frames(OUTPUT_PATH / 'abstract_parser_save_test_data.csv',
                        OUTPUT_PATH / 'abstract_parser_save_test_append_control_data.csv')
    _remove_file(OUTPUT_PATH / 'abstract_parser_save_test_data.csv')


def _assert_data_frames(to_check, control):
    data_to_check = pd.read_csv(to_check, on_bad_lines='skip')
    control_data = pd.read_csv(control, on_bad_lines='skip')

    pd.testing.assert_frame_equal(data_to_check, control_data)


def _remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
