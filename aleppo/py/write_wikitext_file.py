import py.my_open as my_open
from py.book_names import LATIN_TO_HEBREW
from py.my_utils import sl_map
from py.my_utils import sum_of_map


def write_wikitext_file(grouped, out_path):
    lines = sum_of_map(_lines_for_one_book, grouped.items())
    my_open.with_tmp_openw(out_path, {}, _write_callback, lines)


def _lines_for_one_book(bkna_and_entries):
    lat_bkna, entries = bkna_and_entries
    heb_bkna = LATIN_TO_HEBREW[lat_bkna]
    line_1_for_book = "=== " + heb_bkna + " ==="
    line_2_for_book = "'''" + heb_bkna + " ...'''"
    lines_for_entries = sl_map(_lines_for_one_entry, entries)
    return ["", line_1_for_book, line_2_for_book, *lines_for_entries]


def _lines_for_one_entry(entry):
    url = entry["de_url"]
    visible = str(entry["de_text_range"])
    anchor = f"[{url} {visible}]"
    daf_num_ab = entry["de_leaf"]
    daf = f"דף {daf_num_ab}"
    return "#" + anchor + " " + daf


def _write_callback(lines, out_fp):
    for line in lines:
        out_fp.write(line + "\n")
