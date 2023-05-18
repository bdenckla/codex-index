""" Exports main """

import argparse
import my_uxlc
import my_tanakh_book_names as my_tbn
import my_uxlc_page_break_info as page_break_info
from my_uxlc_estimate_location import estimate_location


def _get_uxlc():
    return {bkid: my_uxlc.read(bkid) for bkid in my_tbn.ALL_BOOK_NAMES}


def _get_cite_e_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('book_id', choices=my_tbn.ALL_BOOK_NAMES)
    # e.g. 'Levit'
    parser.add_argument('chapter', type=int)
    parser.add_argument('verse', type=int)
    parser.add_argument('atom', type=int)
    args = parser.parse_args()
    cite_e = args.book_id, args.chapter, args.verse, args.atom
    return cite_e


def main():
    """
    Estimate the concrete location of the given atom.
    """
    cite_e = _get_cite_e_from_args()
    uxlc = _get_uxlc()
    pbi = page_break_info.read_in(uxlc)
    guess_page, guess_fline = estimate_location(uxlc, pbi, cite_e)
    guess_fline_str = f'{guess_fline:.1f}'
    print(guess_page, guess_fline_str)


if __name__ == "__main__":
    main()
