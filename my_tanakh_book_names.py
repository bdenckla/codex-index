"""
This module exports various constants and functions related to naming
the books of the Hebrew Bible and identifying verses within those books.
"""

# Various programs take a --book39tbn argument.
# This comment explains here, centrally, what values are expected for such an
# argument.
# book39tbn is a book name of the following type:
#    * It names a book in the "1 out of 39 books" sense of the word "book".
#         (This is as opposed to the "1 out of 24 books" sense.)
#    * It names these books using our "tbn" convention. The "tbn" convention
#         is encoded here in the my_tanakh_book_names Python module, in constants
#         like FST_SAMUEL.
# A pithy example of a valid value for book39tbn is 1Samuel.
# The example is pithy since:
#    * It shows that this is a "39 books" name, since we identify a "half"
#         of Samuel.
#    * It shows that this is neither the Sefaria nor the UXLC book naming
#         convention: since those would be I Samuel and Samuel_1 respectively.


def book_is_of_sec(in_section, book):
    """ Returns whether the given book belongs to the given section. """
    return _BOOK_PROPERTIES[book][0] == in_section


def books_of_sec(in_section):
    """ Returns a tuple of all book names in the given section. """
    return tuple(b for b in ALL_BOOK_NAMES if book_is_of_sec(in_section, b))


def section(book):
    """ Returns the section to which the given book belongs. """
    return _BOOK_PROPERTIES[book][0]


def ordered_short(book):  # E.g. 'A1' for GENESIS, 'FD' for SND_CHRONICLES
    """
        Returns the ordered short name (2 alphanumerics) corresponding to the
        given book.
        E.g. A1 for Genesis, BA for 1Samuel.
        The 1st alphanumeric is a letter in the range A to F
        corresponding to the book's section.
        The 2nd alphanumeric is a capital Latin letter or base-10 digit.
        This 2nd alphanumeric identifies and orders the book within its
        section.
        ASCII ordering, in particular digits-before-letters ordering,
        is assumed. E.g. B1 (Joshua) comes before BA (1Samuel).
    """
    return _BOOK_PROPERTIES[book][2]


def ordered_short_sena(sena):  # E.g. 'A' for SEC_TORAH, 'B' for SEC_NEV_RISH
    """
        Returns section code A thru F for section with name sena.
    """
    dic = {
        SEC_TORAH: 'A',
        SEC_NEV_RISH: 'B',
        SEC_NEV_AX: 'C',
        SEC_SIF_EM: 'D',
        SEC_XAM_MEG: 'E',
        SEC_KET_ACH: 'F'
    }
    return dic[sena]


def ordered_short_dash_full(bkna):
    """ Return, for example, A1-Genesis given Genesis """
    return f'{ordered_short(bkna)}-{bkna}'


def ordered_short_dash_full_sena(sena):
    """ Return, for example, A-Torah given Torah """
    return f'{ordered_short_sena(sena)}-{sena}'


def short_bcv(bcv):
    """
       Returns, for example, G2:3 for Genesis chapter 2 verse 3.
       Note that, to minimize string length, there is no space between the
       (short) book name and the chapter.
    """
    return short(bcv[0]) + str(bcv[1]) + ':' + str(bcv[2])


def short_bcv2(bkna, chapnver, in_cvjumps):
    """
       Returns a string like short_bcv() but adds:
          a space and a 'c' for a chapter-final (but not book-final) verse
          a space and a 'b' for a book-final verse.
       E.g.:
       1:9 c means
          1:9 is the last verse of its chapter (chapter 1)
          but not the last verse of its book
       8:9 b means
          8:9 is the last verse of its book
    """
    next_cv = cvjumps_next(in_cvjumps, chapnver)
    suff = ''
    if next_cv == 'DNE':
        suff = ' b'
    elif next_cv[0] != chapnver[0]:
        assert next_cv[0] == 1 + chapnver[0] and next_cv[1] == 1
        suff = ' c'
    return short_bcv((bkna, *chapnver)) + suff


def cvjumps(cvs):
    """
        This function returns next verses and previous verses
        for "interesting" verses, i.e. verses for whom next
        or previous isn't simple.
    """
    nexts = {}
    prev_cv = 'DNE'  # does not exist; a "truthy" version of None
    for chapnver in cvs:
        if prev_cv == 'DNE' or chapnver != _simple_next(prev_cv):
            nexts[prev_cv] = chapnver
        prev_cv = chapnver
    if prev_cv:
        nexts[prev_cv] = 'DNE'
    prevs = {x: prev for prev, x in nexts.items()}
    return nexts, prevs


def cvjumps_next(in_cvjumps, cnvnvt):
    """ Return the verse locale after cnvnvt """
    return in_cvjumps[0].get(cnvnvt) or _simple_next(cnvnvt)


def cvjumps_prev(in_cvjumps, cnvnvt):
    """ Return the verse locale before cnvnvt """
    return in_cvjumps[1].get(cnvnvt) or _simple_prev(cnvnvt)


def has_dualcant(bcvtmam):  # bcv in MAM vtrad
    """ Return whether locale bcvt has dual cantillation """
    assert bcvt_is_tmam(bcvtmam)
    return (
        bcvtmam == _SAGA_OF_REUBEN_BCV or
        bcvtmam in _EXDEC_RANGE or
        bcvtmam in _DEDEC_RANGE)


def names_of_books_with_dualcant():
    """ Return the names of the 3 books having dual cantillation """
    return BK_GENESIS, BK_EXODUS, BK_DEUTER


def nu_10(verse_num, vtrad):
    """ Return a bcvt in Numbers chapter 10 """
    cvt = mk_cvt(10, verse_num, vtrad)
    return mk_bcvt(BK_NUMBERS, cvt)


def is_1st_verse_of_decalogue(bcvtmam):
    """
    Return whether bcvtmam is the 1st verse of one of the Decalogues
    """
    assert bcvt_is_tmam(bcvtmam)
    bcv_ex = mk_bcvtmam(BK_EXODUS, 20, 2)
    bcv_de = mk_bcvtmam(BK_DEUTER, 5, 6)
    return bcvtmam in (bcv_ex, bcv_de)


def is_11th_verse_of_decalogue(bcvtmam):
    """
    Return whether bcvtmam is the 11th verse of one of the Decalogues
    """
    assert bcvt_is_tmam(bcvtmam)
    bcv_ex = mk_bcvtmam(BK_EXODUS, 20, 12)
    bcv_de = mk_bcvtmam(BK_DEUTER, 5, 16)
    return bcvtmam in (bcv_ex, bcv_de)


def expand_book_names(book_names):
    """ For each "part 1" book included in booknames,
    add the "part 2" ("next") book.
    """
    nexts = tuple(filter(None, map(next_book_name, book_names)))
    return tuple(set(book_names + tuple(nexts)))


def next_book_name(book_name):
    """ If the named book is part 1 of a 2-part book,
    return the name of part 2. Otherwise return None.
    """
    next_bkna = {  # next book name
        BK_FST_SAMUEL: BK_SND_SAMUEL,
        BK_FST_KINGS: BK_SND_KINGS,
        BK_FST_CHRONICLES: BK_SND_CHRONICLES,
        BK_EZRA: BK_NEXEMIAH,
    }
    return next_bkna.get(book_name)


def mk_bcvtmam(bkna, chnu, vrnu):
    """ Return a bcv qualified with VT_MAM """
    return bkna, chnu, vrnu, VT_MAM


def mk_bcvtsef(bkna, chnu, vrnu):
    """ Return a bcv with vtrad Sef """
    return bkna, chnu, vrnu, VT_SEF


def mk_bcvtbhs(bkna, chnu, vrnu):
    """ Return a bcv with vtrad BHS """
    return bkna, chnu, vrnu, VT_BHS


def mk_bcvt(bkna, cvt):
    """ Make a bcv from a cv """
    return bkna, *cvt


def mk_cvtmam(chnu, vrnu):
    """ Return a cv qualified with VT_MAM """
    return chnu, vrnu, VT_MAM


def mk_cvtsef(chnu, vrnu):
    """ Return a cv with vtrad Sef """
    return chnu, vrnu, VT_SEF


def mk_cvtbhs(chnu, vrnu):
    """ Return a cv with vtrad BHS """
    return chnu, vrnu, VT_BHS


def mk_cvt(chnu, vrnu, vtrad):
    """ Return a cv with the given vtrad """
    return chnu, vrnu, vtrad


def bcvt_get_vtrad(bcvt):
    """ Return the vtrad part of bcvt """
    return bcvt[-1]


def bcvt_is_tmam(bcvt):
    """ Return whether the vtrad is VT_MAM """
    vtrad = bcvt[-1]
    return vtrad == VT_MAM


def bcvt_strip_b(bcvt):
    """ Strip the book name """
    return bcvt[1:]


def bcvt_stript(bcvt):
    """ Strip the vtrad """
    return bcvt[:-1]


def cvt_get_vtrad(cvt):
    """ Return the vtrad part of cvt """
    return cvt[-1]


def cvt_is_tmam(cvt):
    """ Return whether the vtrad is VT_MAM """
    vtrad = cvt[-1]
    return vtrad == VT_MAM


def cvt_is_tsef(cvt):
    """ Return whether the vtrad is vtrad Sef """
    vtrad = cvt[-1]
    return vtrad == VT_SEF


def cvt_stript(cvt):
    """ Strip the vtrad """
    return cvt[:-1]


def short(book):
    """
        Returns the (unordered) short name (1 or 2 letters) corresponding to
        the given book. E.g. G for Genesis, Er for Ezra.
    """
    assert _short_names_are_unique()
    return _short_no_check(book)


def std_from_short(short_book_name):
    """
        Returns the standard book name given the (unordered) short name
        (1 or 2 letters). E.g. Genesis G, Ezra for Er.
    """
    return _SHORT_TO_STD[short_book_name]


def _short_no_check(book):
    return _BOOK_PROPERTIES[book][1]


def _simple_next(cnvnvt):
    return cnvnvt[0], cnvnvt[1] + 1, cnvnvt[2]


def _simple_prev(cnvnvt):
    return cnvnvt[0], cnvnvt[1] - 1, cnvnvt[2]


def _short_names_are_unique():
    unique_shorts = set(map(_short_no_check, ALL_BOOK_NAMES))
    return len(unique_shorts) == len(ALL_BOOK_NAMES)


def _mk_verse_range(bcvt, length):
    vrnu_start = bcvt[2]
    vrange = range(vrnu_start, vrnu_start + length)
    return tuple(_bcvt_setv(bcvt, vrnu) for vrnu in vrange)


def _bcvt_setv(bcvt, new_vrnu):
    return bcvt[0:2] + (new_vrnu,) + bcvt[3:]


BK_GENESIS = 'Genesis'
BK_EXODUS = 'Exodus'
BK_LEVITICUS = 'Levit'
BK_NUMBERS = 'Numbers'
BK_DEUTER = 'Deuter'
BK_JOSHUA = 'Joshua'
BK_JUDGES = 'Judges'
BK_FST_SAMUEL = '1Samuel'
BK_SND_SAMUEL = '2Samuel'
BK_FST_KINGS = '1Kings'
BK_SND_KINGS = '2Kings'
BK_ISAIAH = 'Isaiah'
BK_JEREMIAH = 'Jeremiah'
BK_EZEKIEL = 'Ezekiel'  # guts to change it to Ezeqiel?
BK_HOSEA = 'Hosea'
BK_JOEL = 'Joel'
BK_AMOS = 'Amos'
BK_OBADIAH = 'Obadiah'
BK_JONAH = 'Jonah'
BK_MICAH = 'Micah'  # guts to change it to Mikhah or Miḳah?
BK_NAXUM = 'Nahum'  # guts to change it to Naḥum?
BK_XABAKKUK = 'Habakkuk'  # guts to change it to Ḥabakkuk? Ḥabaqquq?
BK_TSEFANIAH = 'Tsefaniah'
BK_XAGGAI = 'Haggai'  # guts to change it to Ḥaggai?
BK_ZEKHARIAH = 'Zechariah'  # guts to change it to Zekhariah or Zeḳariah?
BK_MALAKHI = 'Malachi'  # guts to change it to Malakhi or Malaḳi?
BK_PSALMS = 'Psalms'
BK_PROVERBS = 'Proverbs'
BK_JOB = 'Job'
BK_SONG_OF_SONGS = 'Song of Songs'
BK_RUTH = 'Ruth'
BK_LAMENTATIONS = 'Lamentations'
BK_ECCLESIASTES = 'Ecclesiastes'
BK_ESTHER = 'Esther'
BK_DANIEL = 'Daniel'
BK_EZRA = 'Ezra'
BK_NEXEMIAH = 'Nehemiah'  # guts to change it to Neḥemiah?
BK_FST_CHRONICLES = '1Chronicles'
BK_SND_CHRONICLES = '2Chronicles'

SEC_TORAH = 'Torah'
SEC_NEV_RISH = 'NevRish'
SEC_NEV_AX = 'NevAḥ'
SEC_SIF_EM = 'SifEm'
SEC_XAM_MEG = 'ḤamMeg'
SEC_KET_ACH = 'KetAḥ'

VT_MAM = 'vtmam'
VT_SEF = 'vtsef'
VT_BHS = 'vtbhs'

_SAGA_OF_REUBEN_BCV = mk_bcvtmam(BK_GENESIS, 35, 22)
_EXDEC_START = mk_bcvtmam(BK_EXODUS, 20, 2)
_DEDEC_START = mk_bcvtmam(BK_DEUTER, 5, 6)
_EXDEC_RANGE = _mk_verse_range(_EXDEC_START, 12)
_DEDEC_RANGE = _mk_verse_range(_DEDEC_START, 12)

_BOOK_PROPERTIES = {
    BK_GENESIS: (SEC_TORAH, 'G', 'A1'),
    BK_EXODUS: (SEC_TORAH, 'E', 'A2'),  # E in contrast to Ee, Ec, Es, Er
    BK_LEVITICUS: (SEC_TORAH, 'L', 'A3'),  # L in contrast to La
    BK_NUMBERS: (SEC_TORAH, 'N', 'A4'),  # N in contrast to Ne & Na
    BK_DEUTER: (SEC_TORAH, 'D', 'A5'),  # D in contrast to Da
    BK_JOSHUA: (SEC_NEV_RISH, 'Js', 'B1'),  # Jo.*: JsJlJnJb
    BK_JUDGES: (SEC_NEV_RISH, 'Ju', 'B2'),
    BK_FST_SAMUEL: (SEC_NEV_RISH, '1S', 'BA'),
    BK_SND_SAMUEL: (SEC_NEV_RISH, '2S', 'BB'),
    BK_FST_KINGS: (SEC_NEV_RISH, '1K', 'BC'),
    BK_SND_KINGS: (SEC_NEV_RISH, '2K', 'BD'),
    BK_ISAIAH: (SEC_NEV_AX, 'I', 'C1'),
    BK_JEREMIAH: (SEC_NEV_AX, 'Je', 'C2'),
    BK_EZEKIEL: (SEC_NEV_AX, 'Ee', 'C3'),  # Ez.*: EeEr
    BK_HOSEA: (SEC_NEV_AX, 'Ho', 'CA'),
    BK_JOEL: (SEC_NEV_AX, 'Jl', 'CB'),  # Jo.*: JsJlJnJb
    BK_AMOS: (SEC_NEV_AX, 'A', 'CC'),
    BK_OBADIAH: (SEC_NEV_AX, 'O', 'CD'),
    BK_JONAH: (SEC_NEV_AX, 'Jn', 'CE'),  # Jo.*: JsJlJnJb
    BK_MICAH: (SEC_NEV_AX, 'Mi', 'CF'),
    BK_NAXUM: (SEC_NEV_AX, 'Na', 'CG'),
    BK_XABAKKUK: (SEC_NEV_AX, 'Hb', 'CH'),  # Ha.*: HbHg
    BK_TSEFANIAH: (SEC_NEV_AX, 'Ts', 'CI'),  # was Zp (see note below)
    BK_XAGGAI: (SEC_NEV_AX, 'Hg', 'CJ'),  # Ha.*: HbHg
    BK_ZEKHARIAH: (SEC_NEV_AX, 'Zc', 'CK'),  # Zc (see note below)
    BK_MALAKHI: (SEC_NEV_AX, 'Ma', 'CL'),
    BK_PSALMS: (SEC_SIF_EM, 'Ps', 'D1'),
    BK_PROVERBS: (SEC_SIF_EM, 'Pr', 'D2'),
    BK_JOB: (SEC_SIF_EM, 'Jb', 'D3'),  # Jo.*: JsJlJnJb
    BK_SONG_OF_SONGS: (SEC_XAM_MEG, 'S', 'E1'),
    BK_RUTH: (SEC_XAM_MEG, 'R', 'E2'),
    BK_LAMENTATIONS: (SEC_XAM_MEG, 'La', 'E3'),
    BK_ECCLESIASTES: (SEC_XAM_MEG, 'Ec', 'E4'),
    BK_ESTHER: (SEC_XAM_MEG, 'Es', 'E5'),
    BK_DANIEL: (SEC_KET_ACH, 'Da', 'F1'),
    BK_EZRA: (SEC_KET_ACH, 'Er', 'FA'),  # Ez.*: EeEr
    BK_NEXEMIAH: (SEC_KET_ACH, 'Ne', 'FB'),
    BK_FST_CHRONICLES: (SEC_KET_ACH, '1C', 'FC'),
    BK_SND_CHRONICLES: (SEC_KET_ACH, '2C', 'FD'),
    # Tsefaniah was formerly Zp because (a) it was formerly spelled Zephaniah
    # and (b) with this former spelling, Ze would have been ambiguous with
    # Zechariah.
    # Zechariah is Zc since Ze would have been ambiguous with Tsefaniah when
    # Tsefaniah was spelled Zephaniah.
}
ALL_BOOK_NAMES = tuple(_BOOK_PROPERTIES.keys())
ALL_SECTION_NAMES = (
    SEC_TORAH, SEC_NEV_RISH, SEC_NEV_AX,
    SEC_SIF_EM, SEC_XAM_MEG, SEC_KET_ACH)
_SHORT_TO_STD = {prop[1]: std for std, prop in _BOOK_PROPERTIES.items()}
