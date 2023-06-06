from enum import Enum
from pathlib import Path


class TweetColumns(Enum):
    USERNAME = 'user_name'
    USERFOLLOWERS = 'user_followers'
    TIMESTAMP = 'timestamp'
    TEXT = 'text'
    RETWEETS = 'retweets'
    USERVERIFIED = 'user_verified'


TWEETS_FILENAME = 'tweets.csv'

SRC_PATH = Path(__file__).absolute().parent
BACKEND_PATH = Path(__file__).absolute().parent.parent
DEST_PATH = BACKEND_PATH / 'res'
