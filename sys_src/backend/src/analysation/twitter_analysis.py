import pandas as pd

from src.analysation import criteria
from sys_src.backend.src.Constants import *


def filter_common_substrings(data: pd.DataFrame):
    # TODO
    return data


def sort_common_substrings(data: pd.DataFrame):
    # TODO
    return data


def sort_follower(data: pd.DataFrame):
    return data.sort_values(by=TweetColumns.USERFOLLOWERS.value, ascending=False)


def sort_user_verified(data: pd.DataFrame):
    return data.sort_values(by=TweetColumns.USERVERIFIED.value, ascending=False)


def calc_points_verified(data: pd.DataFrame, criteria_self):
    data['points'] += data.apply(lambda x: criteria_self.points if x.user_verified else 0)
    return data


def query_relevant_tweets_by_stock(data: pd.DataFrame):
    return criteria.execute_relevant_tweets(data)
