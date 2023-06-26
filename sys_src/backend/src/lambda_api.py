import atexit
import json
import sys_src.backend.stock.stock_data as stock_data
import sys_src.backend.stock.stock_analysis as stock_analysis
import sys_src.backend.twitter.tweet_utils as tweet_utils
import stockbird_logger
from sys_src.backend.src.Constants import *


# define the handler function that the Lambda service will use as an entry point
# TODO: Abfragen der Stock data in eine API-Funktion schreiben, die je nach übergegebenen Parametern die passende Funktion aufruft

logger = stockbird_logger.get_logger(LOGGER_NAME)

def _query_stock_captions(event):
    """Diese Methode gibt alle verfügbaren Stocks mit Symbol und Stock-name zurück."""
    df_json = stock_data.query_stock_captions(event['tree'], SYMBOL_GERMANY_FILENAME, SYMBOL_USA_FILENAME)
    logger.info('Every availlable Stock with Tickers ')
    return json.dumps(df_json)


def _query_stock_data(event):
    df_json = stock_data.query_stocks(event['symbol'], f"stock_{event['symbol']}.json")
    #not sure about the event['symbol']
    logger.info(f'Stock data for" {event["symbol"]}" Ticker')
    return json.dumps(df_json)

def _query_stock_peaks(event):
    df_json = stock_data.query_stocks(event['symbol'], f"stock_{event['symbol']}.json")
    json_file = stock_analysis.query_peaks_from_stock(df_json, event['days'], event['percent'])
    return json_file

def _query_stock_by_date(event):
    df_json = stock_data.query_stocks(event['symbol'], f"stock_{event['symbol']}.json")
    df_filtered = stock_data.query_stock_by_date(df_json, event['date_from'], event['date_to'])
    logger.info(f'Stock data for "{event["symbol"]}" from {event["date_from"]} to {event["date_to"]}')
    return json.dumps(df_filtered.to_dict(orient='records'))


def _query_tweets(event):
    """Diese Funktion gibt alle vorhandenen Tweets aus. Optional kann als Parameter date_from, date_to übergeben werden,
    um die Tweets nach datum einzuschränken"""
    df_json = tweet_utils.query_tweets(TWEETS_FILENAME, event.get('date_from'), event.get('date_to'))
    logger.info('All right now available Tweets')
    return json.dumps(df_json)


def _query_tweets_by_stock(event):
    """Diese Funktion gibt alle Tweets zurück, welche die übergebenen schlagwörter im Text beinhalten.
    Optional kann nach datum eingeschränkt werden"""
    df_json = tweet_utils.query_tweets_by_stock(TWEETS_FILENAME, event.get('date_from'), event['date_to'],
                                                event['substrings'])
    logger.info(f'Tweets concerning "{event["substrings"]}"')
    return json.dumps(df_json)

def _query_tweets_by_stock_info(event):
    """Diese Funktion gibt alle Tweets zurück, welche die übergebenen schlagwörter im Text beinhalten.
    Optional kann nach datum eingeschränkt werden.
    Die Schlagwoerter werden ueber _query_stock_substrings_by_symbol() aus 'stock_info.json' nach event["symbol"] bezogen."""
    df_json = tweet_utils.query_tweets_by_stock(TWEETS_FILENAME, event.get('date_from'), event['date_to'],
                                                stock_data.query_stock_substrings_by_symbol(event['symbol']))
    logger.info(f'Tweets concerning "{event["substrings"]}"')
    return json.dumps(df_json)

def _query_relevant_tweets_by_stock(event):
    """Diese Funktion soll zu dem gegebenen Stock automatisch relevante Tweets returned. Diese Tweets werden nach
       relevanz sortiert zurückgegeben. """
    # TODO wird zu einen späteren Zeitpunkt noch ausprogrammiert! (Analyseebene 3)
    logger.info(f'All Tweets concerning the "{event}" stock')
    return ''

def _query_stock_substrings_by_symbol(event):
    """Diese Funktion soll zu gegebenen stock_symbol die jeweiligen substrings aus dem 'stock_info.json' file,
        aus dem stockbird_res S3 Bucket beziehen und diese als String zurueckgeben"""
    df_json = stock_data.query_stock_substrings_by_symbol(event['symbol'])
    return json.dumps(df_json)

def lambda_handler(event, context):
    atexit.register(stockbird_logger.write_log)
    return {
        'statusCode': 200,
        'body': globals()[event['control']](event)
    }
