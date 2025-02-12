""" Exports main """

from py.group_by_book import group_by_book
from py.read_csv_file import read_csv_file


def main():
    data_entries = read_csv_file(_CSV_IN_PATH, _JSON_OUT_PATH_1)
    group_by_book(data_entries, _JSON_OUT_PATH_2)
    pass


_CSV_IN_PATH = "aleppo/J David Stark Aleppo Codex Index.csv"
_JSON_OUT_PATH_1 = "aleppo/J David Stark Aleppo Codex Index.json"
_JSON_OUT_PATH_2 = "aleppo/index-grouped-by-book.json"


if __name__ == "__main__":
    main()
