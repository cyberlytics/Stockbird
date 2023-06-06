import yfinance
import pandas as pd

import sys_src.backend.src.s3_access as s3

from datetime import date
from datetime import timedelta


# Checks if data is available otherwise the data gets downloaded and saved
def get_data(stock_symbol, file_name):
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

def _is_data_updated(file_name):
    try:
        json_data = s3.read_json(file_name)
        df = pd.DataFrame(json_data)
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

    except:
        return False



