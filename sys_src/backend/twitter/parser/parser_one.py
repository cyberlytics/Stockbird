import argparse

import abstract_parser as ap

from pathlib import Path
from sys_src.backend.Constants import TweetColumns


def _import_data(input_path: Path):
    data = ap.import_data(input_path=input_path,
                          use_cols=[TweetColumns.USERNAME.value, TweetColumns.USERFOLLOWERS.value,
                                    TweetColumns.TEXT.value, TweetColumns.RETWEETS.value,
                                    TweetColumns.USERVERIFIED.value, 'date'],
                          drop_cols=['user_location', 'user_description', 'user_created', 'user_friends',
                                     'user_favourites', 'hashtags', 'is_retweet', 'source', 'id', 'favorites'],
                          rename_cols={'date': TweetColumns.TIMESTAMP.value})

    ap.save(data, header=True if input_path.is_file() else False)


def main():
    """Dieser Parser kann über die Konsole gestartet werden und benötigt den Pfad des zu parsenden csv-Datei."""
    parser = argparse.ArgumentParser(description='Parse csv-file with tweets and add it to tweets.csv.')
    parser.add_argument('-i', '--input-path', type=str,
                        help="path to the directory with data",
                        required=True)

    args = parser.parse_args()

    _import_data(Path(args.input_path))


if __name__ == "__main__":
    main()
