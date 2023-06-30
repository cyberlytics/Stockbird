import pandas as pd

from src.analysation import criteria
from src.stock import stock_data
from sys_src.backend.src.Constants import *


# feste parameter vom frontend
stock_symbol = ''
stock_substrings = ''


# Dieser Abschnitt stell alle benötigten Funktionen für das Berechnen der relevanten Tweets bereit.
def filter_common_substrings(data: pd.DataFrame):
    """Filtert alle Datensätze raus, welche nicht mindestens einen substring enthalten."""
    data = _count_substrings(data)
    return data[data['count_substrings'] > 0]


def sort_common_substrings(data: pd.DataFrame):
    """Sortiert nach der Anzahl an Substrings"""
    return data.sort_values(by='count_substrings', ascending=False)


def _get_common_substrings():
    return stock_data.query_stock_substrings_by_symbol(stock_symbol).split(', ') + stock_substrings.split(', ')


def _count_substrings(data: pd.DataFrame):
    substrings = _get_common_substrings()
    data['count_substrings'] = data.apply(lambda x: sum([x[TweetColumns.TEXT.value].count(val) for val in substrings]),
                                          axis=1)
    return data


def calc_points_common_substrings(data: pd.DataFrame, criteria_self):
    """Berechnet die Punkte für die erreichten substrings und entfernt die vorher dafür hinzugefügte Spalte"""
    data = criteria_self.calc_points(data)
    return data.drop(columns=[criteria_self.column])


def sort_follower(data: pd.DataFrame):
    """Sortiert nach der Anzahl an Followern"""
    return data.sort_values(by=TweetColumns.USERFOLLOWERS.value, ascending=False)


def sort_user_verified(data: pd.DataFrame):
    """Sortiert nach der verification"""
    return data.sort_values(by=TweetColumns.USERVERIFIED.value, ascending=False)


def calc_points_verified(data: pd.DataFrame, criteria_self):
    """Berechnet die Punkte für die verification (True = volle Punktzahl, False = 0 Punkte)"""
    data['points'] += data.apply(lambda x: criteria_self.points if x.user_verified else 0, axis=1)
    return data


def sort_retweets(data: pd.DataFrame):
    """Sortiert nach Retweets"""
    return data.sort_values(by=TweetColumns.RETWEETS.value, ascending=False)


def query_relevant_tweets_by_stock(data: pd.DataFrame, symbol, substrings) -> str:
    """Schnittstelle zur lambda_api.py und zur criteria.py. Diese Methode setzt nur die übergebenen Parameter vom
       Frontend und ruft die entsprechende Methode in criteria.py auf."""
    global stock_symbol, stock_substrings
    stock_symbol = symbol
    stock_substrings = substrings

    return criteria.execute_relevant_tweets(data).to_json(orient='split', index=False, indent=4)
