import json
import stock.stock_data as stock_data
import sys_src.backend.src.Constants as const
import twitter.tweet_utils as tweet_utils
# define the handler function that the Lambda service will use an entry point


def _get_stock_data(event):
    df_json = stock_data.get_data(event['symbol'], f"stock_{event['symbol']}.json")
    df_json_str = json.dumps(df_json)
    return {
        'statusCode': 200,
        'body': df_json_str
    }


def _query_tweets_by_substring(event):
    df_json = tweet_utils.query_tweets_by_substring(const.TWEETS_FILENAME, event['substring'])
    df_json_str = json.dumps(df_json)
    return {
        'statusCode': 200,
        'body': df_json_str
    }


def lambda_handler(event, context):
    return globals()[event['control']](event)
