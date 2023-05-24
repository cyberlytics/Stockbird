import sys
import pandas as pd
from pathlib import Path
backend_path = Path(__file__).absolute().parent.parent.parent
sys.path.append(str(backend_path))
from Constants import TweetColumns

backend_path = Path(__file__).absolute().parent.parent.parent
res_path = backend_path / 'res'


def queryTweetsBySubstring(tweets_file_path: Path, sub_string: str):
    df = pd.read_csv(tweets_file_path)
    df = df[df[TweetColumns.TEXT.value].str.contains(sub_string)]
    df.to_json(res_path / 'tweets_by_stockname.json', orient='split', index=False, indent=4)
