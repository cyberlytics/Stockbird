import datetime
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
SYMBOL_GERMANY_FILENAME = 'SymbolsGermany.csv'
SYMBOL_USA_FILENAME = 'SymbolsUSA.csv'
LOG_FILENAME = f'stockbird-{datetime.date.today().strftime("%Y-%m-%d")}.log'

# All relevant path
SYS_SRC_PATH = Path(__file__).absolute().parent.parent.parent
BACKEND_PATH = Path(__file__).absolute().parent.parent
DEST_PATH = BACKEND_PATH / 'res'
LOGFILE_PATH = DEST_PATH

# Logger specific Constants
LOGGER_NAME = 'stockbird'
LOGGER_FORMATTER = logging.Formatter(
    "%(asctime)s — %(filename)s.%(funcName)20s() — %(levelname)s |***|  %(message)s, |***|")

# S3 specific Constants
ACCESS_KEY_ID = 'AKIATKBDO35QY726HY7J'
ACCESS_KEY = 'vJMAK2okWZrzv1umRgMGKqQ8FHs9NYyAjWDBhVdV'
BUCKET = 'stockbird-res'
