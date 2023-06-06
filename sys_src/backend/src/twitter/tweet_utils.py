from pathlib import Path
import pandas as pd
from sys_src.backend.src.Constants import TweetColumns, DEST_PATH, TWEETS_FILENAME


def query_tweets_by_substring(tweets_file_path: Path, sub_string: str):
    df = pd.read_csv(tweets_file_path)
    df = df[df[TweetColumns.TEXT.value].str.contains(sub_string)]
    df.to_json(DEST_PATH / 'tweets_by_substring.json', orient='split', index=False, indent=4)


def query_tweets_by_user(tweets_file_path: Path, user_name: str):
    df = pd.read_csv(tweets_file_path)
    df = df[df[TweetColumns.USERNAME.value].str.contains(user_name)]
    df.to_json(DEST_PATH / 'tweets_by_username.json', orient='split', index=False, indent=4)
