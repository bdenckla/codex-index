""" Exports main """

from py.read_json_file import read_json_file
from py.group_by_book import group_by_book
from py.write_wikitext_file import write_wikitext_file
import py.my_open as my_open


def main():
    annotated = read_json_file(_JSON_IN_PATH)
    my_open.json_dump_to_file_path(annotated, _JSON_OUT_PATH_1)
    #
    grouped = group_by_book(annotated["body"])
    my_open.json_dump_to_file_path(grouped, _JSON_OUT_PATH_2)
    #
    write_wikitext_file(grouped, _WIKITEXT_OUT_PATH)


_JSON_IN_PATH = "leningrad/out/UXLC-misc/lci_augrecs.json"
_JSON_OUT_PATH_1 = "lenin-wiki/index-flat.json"
_JSON_OUT_PATH_2 = "lenin-wiki/index-grouped-by-book.json"
_WIKITEXT_OUT_PATH = "lenin-wiki/index.wiki"


if __name__ == "__main__":
    main()
