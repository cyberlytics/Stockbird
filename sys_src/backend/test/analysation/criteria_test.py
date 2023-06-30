import json
from pathlib import Path

import pandas as pd

from src.Constants import TweetColumns
from src.analysation import twitter_analysis
from src.analysation.criteria import Criteria

INPUT_PATH = Path(__file__).absolute().parent.parent / 'data/input'
OUTPUT_PATH = Path(__file__).absolute().parent.parent / 'data/output'


def test_criteria_by_sort_followers():
    input_data = pd.read_csv(INPUT_PATH / 'criteria_test.csv', on_bad_lines='skip')
    input_data['points'] = 0

    criteria = Criteria(points=10, column=TweetColumns.USERFOLLOWERS.value, sort_code=twitter_analysis.sort_follower)
    result = criteria.execute(input_data)
    control_data = pd.read_csv(OUTPUT_PATH / 'criteria_test_sort_followers.csv', on_bad_lines='skip')

    assert len(result) == 5
    pd.testing.assert_frame_equal(result, control_data)


def test_criteria_by_filter_followers():
    input_data = pd.read_csv(INPUT_PATH / 'criteria_test.csv', on_bad_lines='skip')
    input_data['points'] = 0

    criteria = Criteria(points=10, column=TweetColumns.USERFOLLOWERS.value, sort_code=twitter_analysis.sort_follower,
                        filter_code=_filter_followers)
    result = criteria.execute(input_data)
    control_data = pd.read_csv(OUTPUT_PATH / 'criteria_test_filter_followers.csv', on_bad_lines='skip')

    assert len(result) == 3
    pd.testing.assert_frame_equal(result, control_data)


def test_criteria_by_followers_calc_points():
    input_data = pd.read_csv(INPUT_PATH / 'criteria_test.csv', on_bad_lines='skip')
    input_data['points'] = 0

    criteria = Criteria(points=10, column=TweetColumns.USERFOLLOWERS.value, sort_code=twitter_analysis.sort_follower,
                        calc_points=_calc_points_follower)
    result = criteria.execute(input_data)

    assert len(result) == 5
    assert len(result[result['points'] == 200000])


def test_two_criteria_by_followers_verified():
    input_data = pd.read_csv(INPUT_PATH / 'criteria_test.csv', on_bad_lines='skip')
    input_data['points'] = 0

    criteria_follower = Criteria(points=10, column=TweetColumns.USERFOLLOWERS.value,
                                 sort_code=twitter_analysis.sort_follower)
    criteria_verified = Criteria(points=2,
                                 column=TweetColumns.USERVERIFIED.value,
                                 sort_code=twitter_analysis.sort_user_verified,
                                 calc_points=twitter_analysis.calc_points_verified)

    result = criteria_follower.execute(input_data)
    result = criteria_verified.execute(result)
    result.sort_values(by='points', inplace=True, ascending=False)
    result.reset_index(inplace=True, drop=True)
    control_data = pd.read_csv(OUTPUT_PATH / 'test_two_criteria_by_followers_verified.csv', on_bad_lines='skip')
    control_data.reset_index(inplace=True, drop=True)

    print(result)
    assert len(result) == 5
    pd.testing.assert_frame_equal(result, control_data)


def _filter_followers(data):
    return data[data[TweetColumns.USERFOLLOWERS.value] >= 101242000]


def _calc_points_follower(data, criteria_self):
    data['points'] += data.apply(lambda x: criteria_self.points * 2, axis=1)
    return data
