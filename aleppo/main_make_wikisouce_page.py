""" Exports main """

import csv
import collections
import re
import py.my_open as my_open


def main():
    with open(_CSV_IN_PATH, encoding="utf-8") as csv_in_fp:
        rows = list(map(_ROW._make, csv.reader(csv_in_fp)))
    assert rows[0] == _EXPECTED_CSV_HEADER
    data_rows = rows[1:]
    assert len(data_rows) == _EXPECTED_LEN_CSV_DATA
    data_entries = list(map(_make_data_entry, data_rows))
    json_header = _make_json_header(data_entries)
    dic_to_dump = {
        "header": json_header,
        "body": data_entries,
    }
    my_open.json_dump_to_file_path(dic_to_dump, _JSON_OUT_PATH)


def _make_json_header(data_entries):
    rows_with_null_url = list(filter(_url_is_none, data_entries))
    rows_with_gap = list(filter(_has_gap, data_entries))
    return {
        "rows_with_null_url": rows_with_null_url,
        "rows_with_gap": rows_with_gap,
    }


def _url_is_none(data_entry):
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
_JSON_OUT_PATH = "aleppo/J David Stark Aleppo Codex Index.json"
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
