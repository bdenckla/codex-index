import py.my_open as my_open
import py.hebrew_verse_numerals as hvn
from py.mam_book_names_and_std_book_names import he_bk39_name
from py.my_utils import sum_of_map, sl_map


def write_wikitext_file(grouped, out_path):
    lines = sum_of_map(_lines_for_one_book, grouped.items())
    my_open.with_tmp_openw(out_path, {}, _write_callback, lines)


def _lines_for_one_book(bkna_and_rows):
    bk39id_mostly, rows = bkna_and_rows
    if bk39id_mostly in (_MAS_LISTS_TORAH, _MAS_LISTS_PROPHETS):
        heb_bkna = bk39id_mostly
        lines_for_rows = sl_map((_line_for_non_bib_row, bk39id_mostly), rows)
    else:
        heb_bkna = he_bk39_name(bk39id_mostly)
        lines_for_rows = sl_map(_line_for_bib_row, rows)
    line_1_for_book = "=== " + heb_bkna + " ==="
    line_2_for_book = "'''" + heb_bkna + " ...'''"
    return ["", line_1_for_book, line_2_for_book, *lines_for_rows]


def _line_for_bib_row(row):
    page = row["page"]
    assert page
    url = f"https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F{page}.jpg"
    visible = _heb_range(_text_range(row))
    anchor = f"[{url} {visible}]"
    daf_num_ab = _cacb_hahb(page)
    daf = f"(דף {daf_num_ab})"
    main_line = "#" + anchor + " " + daf
    return main_line


def _line_for_non_bib_row(visible, row):
    page = row["page"]
    assert page
    url = f"https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F{page}.jpg"
    anchor = f"[{url} {visible}]"
    daf_num_ab = _cacb_hahb(page)
    daf = f"(דף {daf_num_ab})"
    main_line = "#" + anchor + " " + daf
    return main_line


def _text_range(row):
    sta_bcvy = _mref(row, "startc", "startv", "startp", "startl")
    sto_bcvy = _mref(row, "stopc", "stopv", "stopp", "stopl")
    return sta_bcvy, sto_bcvy


def _mref(row, keyc, keyv, keyp, keyl):
    maxp = row[keyl]  # max value of p is the length of the verse
    assert maxp != 1
    if row[keyp] == 1:
        fml = "fml-first"
    elif row[keyp] == row[keyl]:
        fml = "fml-last"
    else:
        fml = "fml-mid"
    return row["bkid"], row[keyc], row[keyv], fml


def _heb_range(text_range):
    sta_bcvy, sto_bcvy = text_range
    sta = _heb_bcv(sta_bcvy[:3])
    sto = _heb_bcv(sto_bcvy[:3])
    sta_str = f'{sta[0]} {sta[1]},{sta[2]}'
    abbr_sto_str = _abbreviated_sto(sta, sto)
    bracs = _brackets(text_range)
    return f"{bracs[0]}{sta_str}{_EN_DASH}{abbr_sto_str}{bracs[1]}"


def _brackets(text_range):
    sta_bcvy, sto_bcvy = text_range
    sta_fml, sto_fml = sta_bcvy[3], sto_bcvy[3]
    sta_brac = "[" if sta_fml == "fml-first" else "("
    sto_brac = "]" if sta_fml == "fml-last" else ")"
    return sta_brac, sto_brac


def _abbreviated_sto(sta, sto):
    if sta[0] == sto[0]:
        if sta[1] == sto[1]:
            return sto[2]
        return f'{sto[1]},{sto[2]}'
    return f'{sto[0]} {sto[1]},{sto[2]}'


def _heb_bcv(bcv):
    bk39id, int_chnu, int_vrnu = bcv
    heb_bkna = he_bk39_name(bk39id)
    heb_chnu = hvn.INT_TO_STR_DIC[int_chnu]
    heb_vrnu = hvn.INT_TO_STR_DIC[int_vrnu]
    return heb_bkna, heb_chnu, heb_vrnu


def _cacb_hahb(leaf):
    # A (ca) (cap A) becomes א (ha) (Hebrew alef)
    # B (cb) (cap B) becomes ב (hb) (Hebrew bet)
    return leaf[:-1] + _CACB_HAHB[leaf[-1]]


def _write_callback(lines, out_fp):
    for line in lines:
        out_fp.write(line + "\n")


_EN_DASH = "–"
_CACB_HAHB = {'A': 'א', 'B': 'ב'}
_MAS_LISTS_TORAH = "Masoretic lists: Number of verses and the sections in the Torah"
_MAS_LISTS_PROPHETS = 'Masoretic lists: Number of verses and the sections in the Prophets'
