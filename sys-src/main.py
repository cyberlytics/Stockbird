import stock_data

if __name__ == '__main__':
    # TODO: When Johnny is done with Symbol list, check if Symbol is available
    stock_symbol = "MSF.DE"
    path = "C:/BKI/04_SOSE 2023/Big Data, Cloud and NoSQL/Stockbird/yFinanceData/" + stock_symbol + ".json"

    df = stock_data.get_data(stock_symbol, path)
    df.to_json(path)
