import json


def read_json_file(json_in_path):
    with open(json_in_path, encoding="utf-8") as json_in_fp:
        rows = json.load(json_in_fp)
    return {"header": _make_json_header(rows), "body": rows}


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
