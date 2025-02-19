import json
import py.my_open as my_open
from py.my_utils import sum_of_map


def read_json_file(json_in_path, json_out_path):
    with open(json_in_path, encoding="utf-8") as json_in_fp:
        data_entries = json.load(json_in_fp)
    my_open.json_dump_to_file_path(_dic_to_dump(data_entries), json_out_path)
    return data_entries


def _dic_to_dump(data_entries):
    json_header = _make_json_header(data_entries)
    dic_to_dump = {
        "header": json_header,
        "body": data_entries,
    }
    return dic_to_dump


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


def _make_json_header(data_entries):
    rows_sans_url = list(filter(_lacks_url, data_entries))
    rows_with_gap = list(filter(_has_gap, data_entries))
    books = _op_unique(sum_of_map(_get_books, data_entries))
    return {
        "rows_sans_url": rows_sans_url,
        "rows_with_gap": rows_with_gap,
        "books": books,
    }
