""" Exports main """

import csv
import collections
import re
import py.my_open as my_open
from py.my_utils import sum_of_map
from py.my_utils import my_groupby
from py.my_utils import dv_map
from py.my_utils import sl_map


def main():
    with open(_CSV_IN_PATH, encoding="utf-8") as csv_in_fp:
        rows = sl_map(_ROW._make, csv.reader(csv_in_fp))
    assert rows[0] == _EXPECTED_CSV_HEADER
    data_rows = rows[1:]
    assert len(data_rows) == _EXPECTED_LEN_CSV_DATA
    data_entries = sl_map(_make_data_entry, data_rows)
    json_header = _make_json_header(data_entries)
    dic_to_dump = {
        "header": json_header,
        "body": data_entries,
    }
    my_open.json_dump_to_file_path(dic_to_dump, _JSON_OUT_PATH_1)
    assigned = sum_of_map(_assign_to_1_or_2_bks, data_entries)
    grouped = my_groupby(assigned, _get_assigned_book)
    unassigned = dv_map(_unassign, grouped)
    my_open.json_dump_to_file_path(unassigned, _JSON_OUT_PATH_2)
    pass


def _unassign(lis_ade):
    return sl_map(_get_data_entry, lis_ade)


def _get_data_entry(ade):  # ade: [book-]assigned data entry
    _assigned_book, data_entry = ade
    return data_entry


def _get_assigned_book(ade):  # ade: [book-]assigned data entry
    assigned_book, _data_entry = ade
    return assigned_book


def _assign_to_1_or_2_bks(data_entry):
    start_bcv, stop_bcv = data_entry["de_text_range"]
    if start_bcv[0] == stop_bcv[0]:
        return [(start_bcv[0], data_entry)]
    return [(start_bcv[0], data_entry), (stop_bcv[0], data_entry)]


def _make_json_header(data_entries):
    rows_sans_url = list(filter(_lacks_url, data_entries))
    rows_with_gap = list(filter(_has_gap, data_entries))
    books = _op_unique(sum_of_map(_get_books, data_entries))
    return {
        "rows_sans_url": rows_sans_url,
        "rows_with_gap": rows_with_gap,
        "books": books
    }


def _get_books(data_entry):
    start_bcv, stop_bcv = data_entry["de_text_range"]
    return [start_bcv[0], stop_bcv[0]]


def _op_unique(lis):  # order-preserving unique
    # Normally, we'd just use set() to remove duplicates,
    # and perhaps sort after, to get a stable (and sensible) order.
    # but here we want to preserve order.
    dic = {}
    for elem in lis:
        dic[elem] = True
    return list(dic.keys())


def _lacks_url(data_entry):
    return data_entry["de_url"] is None


def _has_gap(data_entry):
    return data_entry["de_gap"] is not None


def _make_data_entry(data_row):
    text_range_p = parse_text_range(data_row.text_range)
    if data_row.url_suffix:
        syn_url = _URL_BASE + data_row.url_suffix
        assert syn_url == data_row.bar_hama_2
    else:
        syn_url = None
        assert data_row.bar_hama_2 == ""
    return {
        "de_text_range": text_range_p,
        "de_url": syn_url,
        "de_gap": data_row.gap or None,
    }


def parse_text_range(text_range):
    if match := re.fullmatch(_PATT_FOR_1BK_RANGE, text_range):
        # E.g. Deut 28:17–28:45
        groups = match.groups()
        assert len(groups) == 5
        three_and_three = groups[:3], [groups[0], *groups[3:]]
        return _cv_strs_to_ints_33(three_and_three)
    if match := re.fullmatch(_PATT_FOR_2BK_RANGE, text_range):
        # E.g. Judg 21:15–1 Sam 1:13
        groups = match.groups()
        assert len(groups) == 6
        three_and_three = groups[:3], groups[3:]
        return _cv_strs_to_ints_33(three_and_three)
    assert False, text_range


def _cv_strs_to_ints_33(three_and_three):
    assert len(three_and_three) == 2
    return _cv_strs_to_ints_3(three_and_three[0]), _cv_strs_to_ints_3(three_and_three[1])


def _cv_strs_to_ints_3(three):
    bkna, chnu_str, vrnu_str = three
    return bkna, int(chnu_str), int(vrnu_str)


_URL_BASE = "https://barhama.com/aleppocodex/?image=ALEPPO_CODEX_"  # append url_suffix
_PATT_FOR_BK = r"((?:[12] )?[A-Z][a-z]+)"  # E.g. "1 Sam", "Deut"
_PATT_FOR_CV = r"(\d+):(\d+)"
_PATT_FOR_BCV = _PATT_FOR_BK + " " + _PATT_FOR_CV
_PATT_FOR_1BK_RANGE = _PATT_FOR_BCV + "–" + _PATT_FOR_CV
_PATT_FOR_2BK_RANGE = _PATT_FOR_BCV + "–" + _PATT_FOR_BCV
_CSV_IN_PATH = "aleppo/J David Stark Aleppo Codex Index.csv"
_JSON_OUT_PATH_1 = "aleppo/J David Stark Aleppo Codex Index.json"
_JSON_OUT_PATH_2 = "aleppo/index-grouped-by-book.json"
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
