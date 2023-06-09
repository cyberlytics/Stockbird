import argparse
from abstract_parser import *
from sys_src.backend.src.Constants import TweetColumns


class ParserFive(AbstractParser):

    def __init__(self, source_path: Path):
        super().__init__(source_path)

        self._remove_unused_columns(['user_location', 'user_description',
                                     'user_created', 'user_friends', 'user_favourites',
                                     'hashtags', 'source', 'is_retweet'])
        self._rename_columns({'date': TweetColumns.TIMESTAMP.value})
        self._add_missing_columns([TweetColumns.RETWEETS.value])
        self._change_timestamp_format()
        self._change_column_order([i.value for i in TweetColumns])


def add_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',
                        '--input-path',
                        type=str,
                        required=True,
                        help='Path to the file to be parsed'
                        )
    return parser.parse_args()


def main():
    args = add_args()
    parser = ParserFive(Path(args.input_path))
    parser.append_to_file()
    stockbird_logger.write_log()


if __name__ == "__main__":
    main()
