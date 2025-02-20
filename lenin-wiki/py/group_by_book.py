from py.my_utils import my_groupby


def group_by_book(rows):
    return my_groupby(rows, _get_assigned_book)


def _get_assigned_book(row):
    key = row['bkid'] or row['note']
    assert key is not None
    return key
