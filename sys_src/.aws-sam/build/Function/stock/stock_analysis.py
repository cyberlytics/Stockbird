import json
import pandas as pd

import stock.stock_data as stock_data


def query_peaks_from_stock(str_data: str, days: int, percent: float):

    try:
        json_data = json.loads(str_data)
        df = pd.DataFrame(json_data)
        df = stock_data.reindex_timestamps(df)
    except:
        # add logger
        print("Something is wrong with the data. Return empty list")
        list_peaks = []
        return json.dumps(list_peaks)

    list_peaks = []

    if days <= 0:
        return json.dumps(list_peaks)

    # iterate through the dataframe and check dates that are given days apart
    for i in range(len(df) - days):

        # get the data from current index and the index in days time
        current_difference = _calculate_percent_difference(df.iloc[i].Open, df.iloc[i + days].Open)
        if current_difference > percent or current_difference * -1 > percent:
            dict_peak = {"Start": str(df.index[i]), "End": str(df.index[i + days]), "Difference": current_difference}
            list_peaks.append(dict_peak)

    return json.dumps(list_peaks)


def _calculate_percent_difference(data_start, data_end):
    absolut_diff = data_start - data_end
    percent_diff = (absolut_diff / data_start) * 100
    return percent_diff
