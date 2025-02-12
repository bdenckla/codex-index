import py.my_open as my_open
from py.my_utils import sl_map
from py.my_utils import sum_of_map

def write_wikitext_file(grouped, out_path):
    lines = sum_of_map(_lines_for_one_book, grouped.items())
    my_open.with_tmp_openw(out_path, {}, _write_callback, lines)


def _lines_for_one_book(bkna_and_entries):
    bkna, entries = bkna_and_entries
    line_for_book = bkna
    lines_for_entries = sl_map(_lines_for_one_entry, entries)
    return [line_for_book, *lines_for_entries]


def _lines_for_one_entry(entry):
    return str(entry)


def _write_callback(lines, out_fp):
    for line in lines:
        out_fp.write(line + "\n")
