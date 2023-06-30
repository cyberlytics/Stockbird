import pandas as pd

from sys_src.backend.src.Constants import *
from sys_src.backend.src.analysation import twitter_analysis


def execute_relevant_tweets(data: pd.DataFrame) -> pd.DataFrame:
    """Wird von twitter_analysis.py aufgerufen wenn die relevanten Tweets bewertet werden sollen."""
    return _execute_criteria(data, _get_criteria_relevant_tweets())


def _get_criteria_relevant_tweets():
    """Stellt die Kriterien für die Analyse der relevanten Tweets bereit.
       Achtung man sollte zuerst Kriterien ausführen, welche zusätzlich Filter-Kriterien enthalten, sonst kann das
       Ergebnis verfälscht werden."""
    return [Criteria(points=20,
                     column='count_substrings',
                     sort_code=twitter_analysis.sort_common_substrings,
                     filter_code=twitter_analysis.filter_common_substrings,
                     calc_points=twitter_analysis.calc_points_common_substrings),
            Criteria(points=10,
                     column=TweetColumns.USERFOLLOWERS.value,
                     sort_code=twitter_analysis.sort_follower),
            Criteria(points=2,
                     column=TweetColumns.USERVERIFIED.value,
                     sort_code=twitter_analysis.sort_user_verified,
                     calc_points=twitter_analysis.calc_points_verified),
            Criteria(points=2,
                     column=TweetColumns.RETWEETS.value,
                     sort_code=twitter_analysis.sort_retweets)]


def _execute_criteria(data: pd.DataFrame, criteria_to_execute) -> pd.DataFrame:
    """Basis Methode um von den verschiedenen Schnittstellen (aktuell nur relevante Tweets) die Kriterien auszuführen."""
    data['points'] = 0
    for cr in criteria_to_execute:
        data = cr.execute(data)
    return _sort_remove_points(data)


def _sort_remove_points(data: pd.DataFrame) -> pd.DataFrame:
    """Sortiert nach den erreichten Punkten und entfernt diese am Ende."""
    data.sort_values(by='points', inplace=True, ascending=False)
    return data.drop(columns=['points'])


class Criteria:
    """Diese Klasse wird dafür verwendet, um mit den einzelnen Kriterien umzugehen und zu verwalten. Im Konstruktor
       werden außerdem die aufzurufenden Methoden für das sortieren (verpflichtend), filtern (optional), sowie das
       Kalkulieren der Punkte (optional) übergeben. Diese Methoden können sich auch in einen anderen Modul befinden
       und werden dann intern von der Klasse aufgerufen und ausgeführt."""

    def __init__(self, points: int, column: str, sort_code, filter_code=None, calc_points=None):
        self.points: int = points * 10000
        self.column = column
        self.sort_code = sort_code
        self.filter_code = filter_code
        self.calc_points_ext = calc_points

    def calc_points(self, data: pd.DataFrame) -> pd.DataFrame:
        """Berechnet die erreichten Punkte."""
        data.reset_index(inplace=True, drop=True)
        # TODO diese If ist nur notlösung wegen bugfix, eigentlich sollt der Fall das es keinen Datensatz gibt, welcher
        #  gleich ist gar nicht auftreten!
        data['points'] += data.apply(lambda x: self.points /
                                               (data[data[self.column] == x[self.column]].iloc[0].name + 1)
                                     if len(data[data[self.column] == x[self.column]]) != 0 else 0,
                                     axis=1, result_type='reduce')
        return data

    def execute(self, data: pd.DataFrame) -> pd.DataFrame:
        """Führt alle vorhandenen Methoden aus."""
        if self.filter_code is not None:
            data = self.filter_code(data)
        return self.calc_points_ext(self.sort_code(data), self) if self.calc_points_ext is not None \
            else self.calc_points(self.sort_code(data))
