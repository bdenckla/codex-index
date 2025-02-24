from py.my_utils import my_groupby


def s1_collapse_ranges(rows):
    grouped_by_page = my_groupby(rows, _get_pb)
    return list(map(_collapse_ranges_of_one_page, grouped_by_page.values()))


def _get_pb(row):
    return _get_page(row), _get_book(row)


def _get_page(row):
    return row["page"]


def _get_book(row):
    # We treat the note on a non-Biblical row as a kind of pseudo-book.
    key = row["bkid"] or row["note"]
    assert key is not None
    return key


def _collapse_ranges_of_one_page(ranges_of1p):
    return ranges_of1p[0]
