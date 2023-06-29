from pathlib import Path
from sys_src.backend.src.analysation import twitter_analysis

import pandas as pd

OUTPUT_PATH = Path(__file__).absolute().parent.parent / 'data/output'


def test_query_relevant_tweets_by_stock():
    input_data = pd.read_csv(OUTPUT_PATH / 'parser_one_test_control_data.csv', on_bad_lines='skip')
    print(twitter_analysis.query_relevant_tweets_by_stock(input_data))

