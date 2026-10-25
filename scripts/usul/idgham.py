"""الإدغام الكبير للسوسي (الشاطبية 116–157). Rows: ["idgham", i, flag]; flags: "x" sakin before (ikhfa), "v" across two ayahs."""
from common import *

def mithlayn(w, nxt):
    L = last_letter(w)
    if not L or not nxt: return None
    a, marks = L[-1]
    if a == "ة": a = "ت"
    if not moving(marks): return None
    if a != bare(nxt)[:1]: return None
    if a == "ب" and not bare(w).startswith(("ال", "وال", "فال", "بال")) and (DAMMA in marks or KASRA in marks): return None
    if a == "ت" and letters(w)[-1][0] == "ت": return None
    prev = L[-2] if len(L) >= 2 else None
    return "x" if prev and SUKUN in prev[1] and prev[0] not in "اوي" else ""

def detect(vw):
    out = []
    for key, words, i, nxt, nxc in words_iter(vw):
        r = mithlayn(words[i], nxc)
        if r is not None:
            if nxt is None and not r: r = "v"
            out.append((key, ["idgham", i, r] if r else ["idgham", i]))
        if bare(words[i]) == "مناسككم": out.append((key, ["idgham", i]))
    return out
