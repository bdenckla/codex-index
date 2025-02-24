from py.my_utils import my_groupby


def s1_collapse_ranges(rows):
    return rows
    grouped_by_page = my_groupby(rows, _get_page)
    return list(map(_collapse_ranges_of_one_page, grouped_by_page.values()))


def _get_page(row):
    return row['page']


def _collapse_ranges_of_one_page(ranges_of1p):
    return ranges_of1p[0]
