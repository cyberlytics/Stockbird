import argparse
from abstract_parser import *
from sys_src.backend.Constants import TweetColumns


class ParserTwo(AbstractParser):

    def __init__(self, source_path: Path):
        super().__init__(source_path)
        self._remove_unused_columns(['id', 'url', 'company_names', 'symbols'])
        self._rename_columns({'verified': TweetColumns.USERVERIFIED.value,
                              'source': TweetColumns.USERNAME.value})
        self._add_missing_columns([TweetColumns.RETWEETS.value, TweetColumns.USERFOLLOWERS.value])
        self._change_timestamp_format('%a %b %d %H:%M:%S %z %Y')
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
    parser = ParserTwo(Path(args.input_path))
    parser.append_to_file()


if __name__ == "__main__":
    main()
