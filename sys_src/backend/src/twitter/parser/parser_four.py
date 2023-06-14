import argparse

import sys_src.backend.src.twitter.parser.abstract_parser as ap

from pathlib import Path
from sys_src.backend.src import stockbird_logger
from sys_src.backend.src.Constants import TweetColumns, LOGGER_NAME


def _import_data(input_path: Path, user_name: str = '', user_follower: int = 0, user_verified: bool = False,
                 dest_path=None):
    data = ap.import_data(input_path=input_path,
                          use_cols=[TweetColumns.TIMESTAMP.value, 'tweet', TweetColumns.RETWEETS.value],
                          drop_cols=['id', 'url', 'replies', 'retweets', 'quotes', 'likes'],
                          rename_cols={'date': TweetColumns.TIMESTAMP.value, 'tweet': TweetColumns.TEXT.value})

    ap.save(_format_data(data=data, user_name=user_name, user_follower=user_follower, user_verified=user_verified),
            dest_path=dest_path)


def _format_data(data, user_name: str, user_follower: int, user_verified: bool):
    data[TweetColumns.USERNAME.value] = user_name
    data[TweetColumns.USERFOLLOWERS.value] = user_follower
    data[TweetColumns.USERVERIFIED.value] = user_verified
    stockbird_logger.get_logger(LOGGER_NAME).info(f'User arguments added to data: (user_name={user_name}, '
                                                  f'user_follower={user_follower}, user_verified={user_verified}')
    return data


def main():
    """Dieser Parser kann über die Konsole gestartet werden und benötigt den Pfad des zu parsenden csv-Datei.
       Die Argumente für user-name, user-verified und user-follower sind hingegen optional, falls diese nicht angegeben
       werden, dann wird ein default-value gesetzt."""
    parser = argparse.ArgumentParser(description='Parse csv-file with tweets and add it to tweets.csv.')
    parser.add_argument('-i', '--input-path', type=str,
                        help="path to the directory with data",
                        required=True)
    parser.add_argument('-u', '--user-name', type=str,
                        help="user name that is appended to the file",
                        required=False,
                        default='')
    parser.add_argument('-v', '--user-verified', type=bool,
                        help="user verification that is appended to the file",
                        required=False,
                        default=False)
    parser.add_argument('-f', '--user-followers', type=int,
                        help="number of followers that is appended to the file",
                        required=False,
                        default=0)
    parser.add_argument('-d', '--dest-path', type=str,
                        help="number of followers that is appended to the file",
                        required=False,
                        default=None)

    args = parser.parse_args()

    stockbird_logger.get_logger(LOGGER_NAME).info(f'Parser four started with following arguments: {args}')
    _import_data(Path(args.input_path), args.user_name, args.user_followers, args.user_verified,
                 None if args.dest_path is None else Path(args.dest_path))
    stockbird_logger.write_log()


if __name__ == "__main__":
    main()
