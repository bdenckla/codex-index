import json
import py.my_open as my_open
from py.my_utils import sum_of_map


def read_json_file(json_in_path, json_out_path):
    with open(json_in_path, encoding="utf-8") as json_in_fp:
        rows = json.load(json_in_fp)
    my_open.json_dump_to_file_path(_dic_to_dump(rows), json_out_path)
    return rows


def _dic_to_dump(rows):
    json_header = _make_json_header(rows)
    dic_to_dump = {
        "header": json_header,
        "body": rows,
    }
    return dic_to_dump


def _get_book(row):
    return row["bkid"]


def _runs(lis):
    runs = []
    for elem in lis:
        if runs and runs[-1] == elem:
            continue
        runs.append(elem)
    return runs


def _non_biblical(row):
    return row["bkid"] is None


def _make_json_header(rows):
    non_bib = list(filter(_non_biblical, rows))
    books = _runs(map(_get_book, rows))
    return {
        "rows_non_bib": non_bib,
        "books": books,
    }
