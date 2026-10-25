"""صلة ميم الجمع (الشاطبية 111–115). Rows: ["mim", i] or ["mim", i, "h"] (before hamzat qat': Warsh too)."""
import re
from common import *

def is_plural_mim(w, nxt):
    b, L = bare(w), letters(w)
    if not nxt or not L or L[-1][0] != "م" or (L[-1][1] and SUKUN not in L[-1][1]): return False
    if not re.search(r"(هم|كم|تم)$", b): return False
    if b in ("ثم", "لم", "أم", "يوم", "كم", "وكم", "فكم"): return False
    return not starts_wasl(nxt)

def detect(vw):
    out = []
    for key, words, i, nxt, _ in words_iter(vw):
        if is_plural_mim(words[i], nxt):
            out.append((key, ["mim", i, "h"] if starts_hamza(nxt) else ["mim", i]))
    return out

def mim_before_sakin(w, nxt):
    """ميم الجمع قبل ساكن بعد هاء قبلها كسر أو ياء ساكنة (عَلَيْهِمُ الْقِتَالُ، بِهِمُ الْأَسْبَابُ) — bayts 113–115."""
    if not nxt or not starts_wasl(nxt): return False
    L = letters(w)
    if len(L) < 3 or L[-1][0] != "م" or DAMMA not in L[-1][1] or L[-2][0] != "ه" or KASRA not in L[-2][1]: return False
    return bare(w) not in ("ثم", "لم")

_detect_plain = detect
def detect(vw):
    out = _detect_plain(vw)
    for key, words, i, nxt, _ in words_iter(vw):
        if mim_before_sakin(words[i], nxt): out.append((key, ["mim_sakin", i]))
    return out
