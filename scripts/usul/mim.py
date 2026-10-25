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
