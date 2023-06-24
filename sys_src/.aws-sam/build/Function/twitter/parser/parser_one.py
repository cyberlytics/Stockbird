import argparse

import twitter.parser.abstract_parser as ap

from pathlib import Path
from sys_src.backend.src import stockbird_logger
from sys_src.backend.src.Constants import TweetColumns, LOGGER_NAME


def _import_data(input_path: Path, dest_path=None):
    data = ap.import_data(input_path=input_path,
                          use_cols=[TweetColumns.USERNAME.value, TweetColumns.USERFOLLOWERS.value,
                                    TweetColumns.TEXT.value, TweetColumns.RETWEETS.value,
                                    TweetColumns.USERVERIFIED.value, 'date'],
                          drop_cols=['user_location', 'user_description', 'user_created', 'user_friends',
                                     'user_favourites', 'hashtags', 'is_retweet', 'source', 'id', 'favorites'],
                          rename_cols={'date': TweetColumns.TIMESTAMP.value})

    ap.save(data, dest_path=dest_path)


def main():
    """Dieser Parser kann über die Konsole gestartet werden und benötigt den Pfad des zu parsenden csv-Datei."""
    parser = argparse.ArgumentParser(description='Parse csv-file with tweets and add it to tweets.csv.')
    parser.add_argument('-i', '--input-path', type=str,
                        help="path to the directory with data",
                        required=True)
    parser.add_argument('-d', '--dest-path', type=str,
                        help="number of followers that is appended to the file",
                        required=False,
                        default=None)

    args = parser.parse_args()

    stockbird_logger.get_logger(LOGGER_NAME).info(f'Parser one started with following arguments: {args}')
    _import_data(Path(args.input_path), None if args.dest_path is None else Path(args.dest_path))
    stockbird_logger.write_log()


if __name__ == "__main__":
    main()
