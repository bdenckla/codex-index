"""
This module provides maps (dicts) in both directions between:

    a standard book name like '1Samuel'
    and
    a MAM book name pair like (str('ספר שמואל'), str('שמ"א'))

Note that MAM book names are pairs!
I.e., MAM book names are tuples of length 2.
"""

import py.mam_book_names as mam_book_names
import py.my_locales as tbn


def he_bk39_name(bk39id):
    """
    Given a bk39id, return the corresponding Hebrew bk39 name.
    """
    mam_he_book_name_pair = BK39ID_TO_MAM_HBNP[bk39id]
    return mam_book_names.he_bk39_name(*mam_he_book_name_pair)


def wikisource_book_path_fr_bk39id(bk39id):
    """
    Given bk39id, return the path to the corresponding JSON-format file
    downloaded from Wikisource.
    """
    basename = tbn.ordered_short_dash_full_39(bk39id)
    return f"in/mam-ws/{basename}.json"


def _flip(pair):
    return pair[1], pair[0]


_PAIRS = (
    (mam_book_names.BS_GENESIS, tbn.BK_GENESIS),
    (mam_book_names.BS_EXODUS, tbn.BK_EXODUS),
    (mam_book_names.BS_LEVIT, tbn.BK_LEVIT),
    (mam_book_names.BS_NUMBERS, tbn.BK_NUMBERS),
    (mam_book_names.BS_DEUTER, tbn.BK_DEUTER),
    (mam_book_names.BS_JOSHUA, tbn.BK_JOSHUA),
    (mam_book_names.BS_JUDGES, tbn.BK_JUDGES),
    (mam_book_names.BS_FST_SAM, tbn.BK_FST_SAM),
    (mam_book_names.BS_SND_SAM, tbn.BK_SND_SAM),
    (mam_book_names.BS_FST_KGS, tbn.BK_FST_KGS),
    (mam_book_names.BS_SND_KGS, tbn.BK_SND_KGS),
    (mam_book_names.BS_ISAIAH, tbn.BK_ISAIAH),
    (mam_book_names.BS_JEREM, tbn.BK_JEREM),
    (mam_book_names.BS_EZEKIEL, tbn.BK_EZEKIEL),
    (mam_book_names.BS_HOSEA, tbn.BK_HOSHEA),
    (mam_book_names.BS_JOEL, tbn.BK_JOEL),
    (mam_book_names.BS_AMOS, tbn.BK_AMOS),
    (mam_book_names.BS_OBADIAH, tbn.BK_OVADIAH),
    (mam_book_names.BS_JONAH, tbn.BK_JONAH),
    (mam_book_names.BS_MICAH, tbn.BK_MIKHAH),
    (mam_book_names.BS_NAXUM, tbn.BK_NAXUM),
    (mam_book_names.BS_XABA, tbn.BK_XABA),
    (mam_book_names.BS_TSEF, tbn.BK_TSEF),
    (mam_book_names.BS_XAGGAI, tbn.BK_XAGGAI),
    (mam_book_names.BS_ZEKHAR, tbn.BK_ZEKHAR),
    (mam_book_names.BS_MALAKHI, tbn.BK_MALAKHI),
    (mam_book_names.BS_PSALMS, tbn.BK_PSALMS),
    (mam_book_names.BS_PROV, tbn.BK_PROV),
    (mam_book_names.BS_JOB, tbn.BK_JOB),
    (mam_book_names.BS_SONG, tbn.BK_SONG),
    (mam_book_names.BS_RUTH, tbn.BK_RUTH),
    (mam_book_names.BS_LAMENT, tbn.BK_LAMENT),
    (mam_book_names.BS_QOHELET, tbn.BK_QOHELET),
    (mam_book_names.BS_ESTHER, tbn.BK_ESTHER),
    (mam_book_names.BS_DANIEL, tbn.BK_DANIEL),
    (mam_book_names.BS_EZRA, tbn.BK_EZRA),
    (mam_book_names.BS_NEXEM, tbn.BK_NEXEM),
    (mam_book_names.BS_FST_CHR, tbn.BK_FST_CHR),
    (mam_book_names.BS_SND_CHR, tbn.BK_SND_CHR),
)
BK39ID_TO_MAM_HBNP = dict(map(_flip, _PAIRS))
MAM_HBNP_TO_BK39ID = dict(_PAIRS)
