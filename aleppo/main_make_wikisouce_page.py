""" Exports main """

from py.read_csv_file import read_csv_file
from py.group_by_book import group_by_book
from py.write_wikitext_file import write_wikitext_file


def main():
    data_entries = read_csv_file(_CSV_IN_PATH, _JSON_OUT_PATH_1)
    grouped = group_by_book(data_entries, _JSON_OUT_PATH_2)
    write_wikitext_file(grouped, _WIKITEXT_OUT_PATH)
    pass


_CSV_IN_PATH = "aleppo/J David Stark Aleppo Codex Index.csv"
_JSON_OUT_PATH_1 = "aleppo/index-flat.json"
_JSON_OUT_PATH_2 = "aleppo/index-grouped-by-book.json"
_WIKITEXT_OUT_PATH = "aleppo/index.wiki"


if __name__ == "__main__":
    main()
