import json

import yfinance
import pandas as pd

import sys_src.backend.src.s3_access as s3

from datetime import date
from datetime import timedelta

import datetime


# Checks if data is available otherwise the data gets downloaded and saved
def get_data(stock_symbol: str, file_name: str):
    # check if data is updated
    if _is_data_updated(file_name):
        json_data = s3.read_json(file_name)
        return json_data
    else:
        #get data and save in a dataframe
        ticker = yfinance.Ticker(stock_symbol)
        data = ticker.history(period='max', interval='1d')
        df_json = pd.DataFrame(data).to_json()
        s3.write_json(df_json, file_name)
        return df_json


def query_stock_captions(tree: bool, *file_names):
    """return all stock-symbols and stock-names to the available stocks."""
    # TODO tree muss noch ausprogrammiert werden.
    return_data = pd.DataFrame()
    for file_name in file_names:
        return_data = pd.concat([return_data, s3.read_csv(file_name=file_name)])

    return return_data.to_json(orient='split', index=False, indent=4)


def _is_data_updated(file_name: str):
    try:
        json_data = s3.read_json(file_name)
        json_data = json.loads(json_data)

        df = pd.DataFrame(json_data)
        df = _reindex_timestamps(df)

        today = date.today()
        # if today is a monday, the last available data from yfinance should be friday today - 3 days
        if today.weekday() == 0:
            most_recent_day = today - timedelta(days=3)
        # else, the last available data should be from yesterday -1 day
        else:
            most_recent_day = today - timedelta(days=1)

        # yfinance only downloads data from one day ago
        return df.index[-1] == most_recent_day

    except:
        return False


def _reindex_timestamps(df: pd.DataFrame):
    dt_index = []

    for timestamp_ms in df.index:
        timestamp_sec = int(timestamp_ms) / 1000  # Convert milliseconds to seconds

        # Create a datetime object from the timestamp
        dt = datetime.datetime.utcfromtimestamp(timestamp_sec).date()

        # Print the datetime object
        dt_index.append(dt)

    df = df.set_index(pd.Index(dt_index))

    return df


def filter_by_date(to_filter: str, from_date: str, to_date: str):
    dt_from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
    dt_to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()

    json_data = json.loads(to_filter)
    df = pd.DataFrame(json_data)
    df = _reindex_timestamps(df)

    filtered_df = df.loc[(df.index >= dt_from_date) & (df.index <= dt_to_date)]

    return filtered_df
