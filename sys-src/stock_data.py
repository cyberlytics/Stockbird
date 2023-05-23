import yfinance
import pandas as pd
from datetime import date


def get_data(stock_symbol, path):
    # check if data is updated
    if is_data_updated(stock_symbol, path):
        print("no update")
        return

    else:
        print("update")
        # get data and save in a dataframe
        ticker = yfinance.Ticker(stock_symbol)
        data = ticker.history(period='max', interval='1d')
        return pd.DataFrame(data)


def is_data_updated(stock_symbol, path):
    # try to find data on local machine
    try:
        df = pd.read_json(path)
        df.index = df.index.strftime('%Y-%m-%d')

        return df.index[-1] == str(date.today())

    except FileNotFoundError:
        return False



