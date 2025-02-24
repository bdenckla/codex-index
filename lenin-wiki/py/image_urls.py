def image_urls(page_ddda):
    # page asssumed to be in DDDA format, meaning 3 digits followed by A or B, e.g. 043B.
    page_n = _get_page_n(page_ddda)
    return {
        "sefa": f"{_PRE_SEFA}BIB_LENCDX_F{page_ddda}.jpg",
        "lcci": f"{_PRE_LCCI}n{page_n}/mode/1up?view=theater",
    }


def _get_page_n(page_ddda):
    assert len(page_ddda) == 4
    part_ddd_str = page_ddda[:3]
    part_a = page_ddda[3]
    part_dd_int = int(part_ddd_str)
    assert 1 <= part_dd_int <= 463
    page_n_naive = 2 * part_dd_int + _AB_INT[part_a]
    # Below, we substract 2 because "naively", ddda="001B" maps to n=3 (2*1 + 1)
    # but we want it to map to n=1.
    return page_n_naive - 2


_AB_INT = {"A": 0, "B": 1}
_PRE_SEFA = "https://manuscripts.sefaria.org/leningrad-color/"
_PRE_LCCI = "https://archive.org/details/Leningrad_Codex_Color_Images/page/"
