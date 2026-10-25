"""الإمالة الكبرى لحمزة والكسائي في ذوات الياء (الشاطبية 291–336). Rows: ["imala", i, flag]; flags: "w" pause only, "k" al-Kisa'i only, "dk" al-Duri 'an al-Kisa'i only."""
import re
from common import *

NOT_IMALA = {"على", "إلى", "حتى", "لدى"}
ALIF_WORDS = {"الدنيا": "", "والدنيا": "", "بالدنيا": "", "الربا": "", "الربواا": "", "والربواا": "", "بسيماهم": "", "سيماهم": "",
              "خطاياكم": "k", "مرضات": "k", "مرضاة": "k", "فأحياكم": "k", "أحياكم": "k", "فأحيا": "k", "أحياهم": "k", "هداي": "dk"}

def kubra(w, nxt):
    b = bare(w)
    if b in ALIF_WORDS: return ALIF_WORDS[b]
    if re.search(r"ى(ه|هم|هما|هن|ها|ك|كم|نا|ني)$", b): return ""
    if not b.endswith("ى"): return None
    if b in NOT_IMALA or re.sub(r"^(و|ف)", "", b) in NOT_IMALA: return None
    L = letters(w)
    before = L[-2][1] if len(L) >= 2 else ""
    if FATHA not in before or (nxt is not None and starts_wasl(nxt)): return "w"
    return ""

def detect(vw):
    out = []
    for key, words, i, nxt, _ in words_iter(vw):
        r = kubra(words[i], nxt)
        if r is not None: out.append((key, ["imala", i, r] if r else ["imala", i]))
    return out
