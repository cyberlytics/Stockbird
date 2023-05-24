from enum import Enum


class TweetColumns(Enum):
    USERNAME = 'user_name'
    USERFOLLOWERS = 'user_followers'
    TIMESTAMP = 'timestamp'
    TEXT = 'text'
    RETWEETS = 'retweets'
    USERVERIFIED = 'user_verified'
