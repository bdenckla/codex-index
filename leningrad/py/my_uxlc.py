""" Exports read_all_books, read. """

import xml.etree.ElementTree

import my_tanakh_book_names as tbn


def read_all_books(handlers=None):
    return {bkid: read(bkid, handlers) for bkid in tbn.ALL_BOOK_IDS}


def read(book_id, handlers=None):
    """Read book with id book_id into a list of chapters."""
    handlers = handlers or _VERSE_CHILD_HANDLERS
    basename = _UXLC_BOOK_FILE_NAMES[book_id]
    xml_path = f"in/UXLC/{basename}.xml"
    tree = xml.etree.ElementTree.parse(xml_path)
    root = tree.getroot()
    chapters = []
    for chapter in root.iter("c"):
        verses = []
        for verse in chapter.iter("v"):
            words = []
            for verse_child in verse:
                dispatch_on_tag(words, verse_child, handlers)
            verses.append(words)
        chapters.append(verses)
    return chapters


def handle_xc_ignore(_1, _2):  # xc means vc or wc (verse child or word child)
    return


def dispatch_on_tag(accum, xml_element, handlers):
    fn_for_tag = handlers[xml_element.tag]
    fn_for_tag(accum, xml_element)


def _handle_wc_s(accum, word_child_s):
    # The <s> element implements small, large, and suspended letters.
    # E.g. <s t="large">וֹ</s>.
    accum[-1] += word_child_s.text.strip()


def _handle_vc_wq(accum, verse_child_wq):
    accum.append(verse_child_wq.text.strip())
    for word_child in verse_child_wq:
        dispatch_on_tag(accum, word_child, _WORD_CHILD_HANDLERS)
        accum[-1] += word_child.tail.strip()


_WORD_CHILD_HANDLERS = {
    "x": handle_xc_ignore,
    "s": _handle_wc_s,
}
_VERSE_CHILD_HANDLERS = {
    "w": _handle_vc_wq,
    "q": _handle_vc_wq,
    "k": handle_xc_ignore,
    "x": handle_xc_ignore,
    "pe": handle_xc_ignore,
    "samekh": handle_xc_ignore,
    "reversednun": handle_xc_ignore,
}
_UXLC_BOOK_FILE_NAMES = {
    tbn.BK_GENESIS: "Genesis",
    tbn.BK_EXODUS: "Exodus",
    tbn.BK_LEVIT: "Leviticus",
    tbn.BK_NUMBERS: "Numbers",
    tbn.BK_DEUTER: "Deuteronomy",
    tbn.BK_JOSHUA: "Joshua",
    tbn.BK_JUDGES: "Judges",
    tbn.BK_FST_SAM: "Samuel_1",
    tbn.BK_SND_SAM: "Samuel_2",
    tbn.BK_FST_KGS: "Kings_1",
    tbn.BK_SND_KGS: "Kings_2",
    tbn.BK_ISAIAH: "Isaiah",
    tbn.BK_JEREM: "Jeremiah",
    tbn.BK_EZEKIEL: "Ezekiel",
    tbn.BK_HOSHEA: "Hosea",
    tbn.BK_JOEL: "Joel",
    tbn.BK_AMOS: "Amos",
    tbn.BK_OVADIAH: "Obadiah",
    tbn.BK_JONAH: "Jonah",
    tbn.BK_MIKHAH: "Micah",
    tbn.BK_NAXUM: "Nahum",
    tbn.BK_XABA: "Habakkuk",
    tbn.BK_TSEF: "Zephaniah",
    tbn.BK_XAGGAI: "Haggai",
    tbn.BK_ZEKHAR: "Zechariah",
    tbn.BK_MALAKHI: "Malachi",
    tbn.BK_PSALMS: "Psalms",
    tbn.BK_PROV: "Proverbs",
    tbn.BK_JOB: "Job",
    tbn.BK_SONG: "Song_of_Songs",
    tbn.BK_RUTH: "Ruth",
    tbn.BK_LAMENT: "Lamentations",
    tbn.BK_QOHELET: "Ecclesiastes",
    tbn.BK_ESTHER: "Esther",
    tbn.BK_DANIEL: "Daniel",
    tbn.BK_EZRA: "Ezra",
    tbn.BK_NEXEM: "Nehemiah",
    tbn.BK_FST_CHR: "Chronicles_1",
    tbn.BK_SND_CHR: "Chronicles_2",
}
