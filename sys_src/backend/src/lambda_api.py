import atexit
import json
import stock.stock_data as stock_data
import twitter.tweet_utils as tweet_utils
from sys_src.backend.src import stockbird_logger
from sys_src.backend.src.Constants import *


# define the handler function that the Lambda service will use as an entry point


def _query_stock_captions(event):
    """Diese Methode gibt alle verfügbaren Stocks mit Symbol und Stock-name zurück."""
    df_json = stock_data.query_stock_captions(event['tree'], SYMBOL_GERMANY_FILENAME, SYMBOL_USA_FILENAME)
    return json.dumps(df_json)


def _query_stock_data(event):
    df_json = stock_data.query_stocks(event['symbol'], f"stock_{event['symbol']}.json")
    return json.dumps(df_json)


def _query_stock_by_date(event):
    df_json = stock_data.query_stocks(event['symbol'], f"stock_{event['symbol']}.json")
    df_filtered = stock_data.query_stock_by_date(df_json, event['from_date'], event['to_date'])
    return json.dumps(df_filtered)


def _query_tweets_by_stock_name(event):
    df_json = tweet_utils.query_tweets_by_stock_name(TWEETS_FILENAME, event['stock_name'])
    return json.dumps(df_json)


def _query_relevant_tweets_by_stock(event):
    """Diese Funktion soll zu dem gegebenen Stock automatisch relevante Tweets returned. Diese Tweets werden nach
       relevanz sortiert zurückgegeben. """
    # TODO wird zu einen späteren Zeitpunkt noch ausprogrammiert! (Analyseebene 3)
    return ''


def lambda_handler(event, context):
    atexit.register(stockbird_logger.write_log())
    return {
        'statusCode': 200,
        'body': globals()[event['control']](event)
    }
