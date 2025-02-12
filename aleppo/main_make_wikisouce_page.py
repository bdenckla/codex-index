""" Exports main """

import csv
import collections
import re


def main():
    with open(_CSV_PATH, encoding="utf-8") as csv_in_fp:
        rows = list(map(_ROW._make, csv.reader(csv_in_fp)))
    assert rows[0] == _EXPECTED_CSV_HEADER
    data_rows = rows[1:]
    assert len(data_rows) == _EXPECTED_LEN_CSV_DATA
    data_entries = list(map(_make_data_entry, data_rows))
    pass


def _make_data_entry(data_row):
    text_range_p = parse_text_range(data_row.text_range)
    return text_range_p


def parse_text_range(text_range):
    # E.g. Deut 28:17–28:45
    if match := re.fullmatch(_PATT_FOR_1BK_RANGE, text_range):
        groups = match.groups()
        return groups
    if match := re.fullmatch(_PATT_FOR_2BK_RANGE, text_range):
        groups = match.groups()
        print(groups)
        return groups
    assert False, text_range


_PATT_FOR_BK = r"((?:[12] )?[A-Z][a-z]+)"
_PATT_FOR_CV = r"(\d+):(\d+)"
_PATT_FOR_BCV = _PATT_FOR_BK + " " + _PATT_FOR_CV
_PATT_FOR_1BK_RANGE = _PATT_FOR_BCV + "–" + _PATT_FOR_CV
_PATT_FOR_2BK_RANGE = _PATT_FOR_BCV + "–" + _PATT_FOR_BCV
_CSV_PATH = "aleppo/J David Stark Aleppo Codex Index.csv"
_ROW_FIELD_NAMES = "text_range,leaf,page,bar_hama_2,gap,notes,url_suffix"
_ROW = collections.namedtuple("_ROW", _ROW_FIELD_NAMES)
_EXPECTED_CSV_HEADER_VALS = (
    "Text Range",
    "Leaf",
    "Page",
    "Bar Hama 2",
    "Gap",
    "Notes",
    "URL-suffix"
)
_EXPECTED_CSV_HEADER = _ROW._make(_EXPECTED_CSV_HEADER_VALS)
_EXPECTED_LEN_CSV_DATA = 590


if __name__ == "__main__":
    main()
