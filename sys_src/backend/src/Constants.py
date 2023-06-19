from enum import Enum
from pathlib import Path
import logging


class TweetColumns(Enum):
    USERNAME = 'user_name'
    USERFOLLOWERS = 'user_followers'
    TIMESTAMP = 'timestamp'
    TEXT = 'text'
    RETWEETS = 'retweets'
    USERVERIFIED = 'user_verified'


# All relevant file names
TWEETS_FILENAME = 'tweets.csv'
LOG_FILENAME = f'stockbird.log'

# All relevant path
SRC_PATH = Path(__file__).absolute().parent.parent
BACKEND_PATH = Path(__file__).absolute().parent
DEST_PATH = BACKEND_PATH / 'res'
LOGFILE_PATH = DEST_PATH

# Logger specific Constants
LOGGER_NAME = 'stockbird'
LOGGER_FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s, "
                                     "[ %(filename)s.%(funcName)20s() ]")
