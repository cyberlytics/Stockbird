import yfinance
import pandas as pd

from datetime import date
from datetime import timedelta


# Checks if data is available otherwise the data gets downloaded and saved
def get_data(stock_symbol, path):
    # check if data is updated
    if is_data_updated(path):
        return

    else:
        # get data and save in a dataframe
        ticker = yfinance.Ticker(stock_symbol)
        data = ticker.history(period='max', interval='1d')
        pd.DataFrame(data).to_json(path)


def is_data_updated(path):
    try:
        df = pd.read_json(path)
        df.index = df.index.strftime('%Y-%m-%d')

        today = date.today()
        # if today is a monday, the last available data from yfinance should be friday today - 3 days
        if today.weekday() == 0:
            most_recent_day = today - timedelta(days=3)
        # else, the last available data should be from yesterday -1 day
        else:
            most_recent_day = today - timedelta(days=1)

        # yfinance only downloads data from yesterday
        return df.index[-1] == str(most_recent_day)

    except FileNotFoundError:
        return False



