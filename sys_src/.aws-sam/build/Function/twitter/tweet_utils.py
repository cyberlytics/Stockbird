import backend.src.s3_access as s3
import pandas as pd
from backend.src.Constants import TweetColumns, DEST_PATH


def query_tweets_by_substring(tweets_file_name, sub_string: str):
    print("File_name: ", tweets_file_name)
    print("Substring: ", sub_string)
    df = pd.DataFrame(s3.read_csv(tweets_file_name))
    print("Made it past the retrieval!")
    df = df[df[TweetColumns.TEXT.value].str.contains(sub_string)]
    print("Made it past the Filtering!")
    df_json = df.to_json(orient='split', index=False, indent=4)
    print("Made it past the json_converter!")
    return df_json

def query_tweets_by_user(tweets_file_name, user_name: str):
    df = pd.read_csv(tweets_file_name)
    df = df[df[TweetColumns.USERNAME.value].str.contains(user_name)]
    df.to_json(DEST_PATH / 'tweets_by_username.json', orient='split', index=False, indent=4)
