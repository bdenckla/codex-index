""" Exports main """

from py.read_json_file import read_json_file
from py.group_by_book import group_by_book
from py.write_wikitext_file import write_wikitext_file


def main():
    data_entries = read_json_file(_JSON_IN_PATH, _JSON_OUT_PATH_1)
    grouped = group_by_book(data_entries, _JSON_OUT_PATH_2)
    write_wikitext_file(grouped, _WIKITEXT_OUT_PATH)


_JSON_IN_PATH = "leningrad/out/UXLC-misc/lci_augrecs.json"
_JSON_OUT_PATH_1 = "lenin-wiki/index-flat.json"
_JSON_OUT_PATH_2 = "lenin-wiki/index-grouped-by-book.json"
_WIKITEXT_OUT_PATH = "lenin-wiki/index.wiki"


if __name__ == "__main__":
    main()
