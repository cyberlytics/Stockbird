import yfinance
import pandas as pd
from datetime import date


def get_data(stock_symbol):
    # check if data is updated
    # if is_data_updated(stock_symbol):
    #    return

    #else:
    ticker = yfinance.Ticker(stock_symbol)
    data = ticker.history(period='max', interval='1d')

    df = pd.DataFrame(data)
    print(df)

    #try:
    #    df.to_csv("C:/BKI/04_SOSE 2023/Big Data, Cloud and NoSQL/Stockbird/yFinanceData/" + stock_symbol + ".csv")
        #update_data_info(stock_symbol)
    #except PermissionError:
    #    print("The csv file might be opened on your system.")
    #    return

    #update_data_info(stock_symbol)



def update_data_info(stock_symbol):
    data_info = pd.read_csv("C:/BKI/04_SOSE 2023/Big Data, Cloud and NoSQL/Stockbird/yFinanceData/data_information.csv")

    # iterate through the dataframe and update the date
    for ind in data_info.index:
        if data_info["symbol"][ind] == stock_symbol:
            data_info["updated"][ind] = date.today()
            return

    data_info.append({"symbol": stock_symbol, "updated": date.today()})
    data_info.to_csv("C:/BKI/04_SOSE 2023/Big Data, Cloud and NoSQL/Stockbird/yFinanceData/data_information.csv")


def is_data_updated(stock_symbol):
    data_info = pd.read_csv("C:/BKI/04_SOSE 2023/Big Data, Cloud and NoSQL/Stockbird/yFinanceData/data_information.csv")

    for ind in data_info.index:
        if data_info["symbol"][ind] == stock_symbol:
            if data_info["updated"][ind] == date.today():
                return True
            else:
                return False

    return False
