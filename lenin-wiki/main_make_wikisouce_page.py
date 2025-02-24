""" Exports main """

from py.read_json_file import read_json_file
from py.s1_collapse_ranges import s1_collapse_rows
from py.s2_group_by_book import s2_group_by_book
from py.write_wikitext_file import write_wikitext_file
import py.my_open as my_open


def main():
    annotated = read_json_file(_JSON_IN_PATH)
    my_open.json_dump_to_file_path(annotated, _JSON_OUT_PATH_S0)
    #
    s1_collapsed = s1_collapse_rows(annotated["body"])
    #
    s2_grouped = s2_group_by_book(s1_collapsed)
    my_open.json_dump_to_file_path(s2_grouped, _JSON_OUT_PATH_S2)
    #
    write_wikitext_file(s2_grouped, _WIKITEXT_OUT_PATH)


_JSON_IN_PATH = "leningrad/out/UXLC-misc/lci_augrecs.json"
_JSON_OUT_PATH_S0 = "lenin-wiki/index-s0-annotated.json"
_JSON_OUT_PATH_S2 = "lenin-wiki/index-s2-grouped-by-book.json"
_WIKITEXT_OUT_PATH = "lenin-wiki/index.wiki"


if __name__ == "__main__":
    main()
