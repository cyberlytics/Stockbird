import pandas as pd

from sys_src.backend.src.Constants import *
from sys_src.backend.src.analysation import twitter_analysis

_relevant_tweets_criteria = []


# relevant tweets
def execute_relevant_tweets(data: pd.DataFrame) -> pd.DataFrame:
    return _execute_criteria(data, _get_criteria_relevant_tweets())


def _get_criteria_relevant_tweets():
    if not _relevant_tweets_criteria:
        # you need to run all filter criteria, before only sort criteria
        # _relevant_tweets_criteria.append(Criteria(5, sort_common_substrings, filter_common_substrings))
        _relevant_tweets_criteria.append(Criteria().__int__(5, twitter_analysis.sort_follower, None, None))
        _relevant_tweets_criteria.append(Criteria().__int__(5, twitter_analysis.sort_user_verified,
                                                            twitter_analysis.calc_points_verified, None))
    return _relevant_tweets_criteria


def _execute_criteria(data: pd.DataFrame, criteria_to_execute) -> pd.DataFrame:
    data['points'] = 0
    for cr in criteria_to_execute:
        data = cr.execute(data)
    return data
    # return _sort_remove_points(data)


def _sort_remove_points(data: pd.DataFrame) -> pd.DataFrame:
    data.sort_values(by='points', inplace=True, ascending=False)
    return data.drop(columns=['points'], inplace=True)


class Criteria:

    def __int__(self, points: int, sort_code, filter_code: None, calc_points: None):
        self.points: int = points * 10000
        self.sort_code = sort_code
        self.filter_code = filter_code
        self.calc_points = calc_points
        return self

    def _calc_points(self, data: pd.DataFrame) -> pd.DataFrame:
        # TODO funkitoniert noch nicht
        print("data")
        print(data)
        data['points'] += data.apply(lambda x: self.points / x.index)
        return data

    def execute(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.filter_code is not None:
            data = self.filter_code(data)
        return self.calc_points(self.sort_code(data)) if self.calc_points is not None \
            else self._calc_points(self.sort_code(data))
