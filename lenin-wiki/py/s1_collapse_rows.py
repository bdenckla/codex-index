from py.my_utils import my_groupby


def s1_collapse_rows(rows):
    grouped_by_pb = my_groupby(rows, _get_pb)
    return list(map(_collapse_rows_of_one_pb, grouped_by_pb.values()))


def _get_pb(row):
    # pb: page/book pair
    return _get_page(row), _get_book(row)


def _get_page(row):
    return row["page"]


def _get_book(row):
    # We treat the note on a non-Biblical row as a kind of pseudo-book.
    key = row["bkid"] or row["note"]
    assert key is not None
    return key


def _collapse_rows_of_one_pb(rows_of1pb):
    # pb: page/book pair
    if len(rows_of1pb) == 1:
        return rows_of1pb[0]
    row1, row2 = rows_of1pb[0], rows_of1pb[1]
    sto_r1 = _sto_cvp(row1)
    sta_r2 = _sta_cvp(row2)
    assert _is_next(sto_r1, sta_r2)
    collapsed = _set_sto(row1, _sto_cvp(row2))
    return collapsed


def _is_next(cvp1, cvp2):
    return cvp2 in _nexts(cvp1)


def _nexts(cvp):
    return ((cvp[0], cvp[1], cvp[2] + 1), (cvp[0], cvp[1] + 1, 1), (cvp[0] + 1, 1, 1))


def _sta_cvp(row):
    return _get3(row, *_STA_KEYS)


def _sto_cvp(row):
    return _get3(row, *_STO_KEYS)


def _set_sta(row, cvp): return _ovr(row, _STA_KEYS, cvp)


def _set_sto(row, cvp): return _ovr(row, _STO_KEYS, cvp)


_STA_KEYS = "startc", "startv", "startp"
_STO_KEYS = "stopc", "stopv", "stopp"


def _get3(row, keyc, keyv, keyp):
    return row[keyc], row[keyv], row[keyp]


def _ovr(row, ovr_keys, ovr_vals):
    overrides = dict(zip(ovr_keys, ovr_vals))
    return {**row, **overrides}
