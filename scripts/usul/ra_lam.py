"""ترقيق ورش للراءات (الشاطبية 343–358) وتغليظه للامات (359–362).
Rows: ["ra_warsh", i] or ["ra_warsh", i, "kh"] (the six words ذكرا سترا إمرا وزرا حجرا صهرا: both, tafkhim preferred);
      ["lam_warsh", i] or ["lam_warsh", i, flag]; flags: "a" alif between (طال، فصالا), "w" final lam (pause: both),
      "y" a dhawat al-ya alif follows (مصلّى: pause = taghlith+fath or tarqiq+taqlil)."""
import re
from common import *

ISTILA = "قظخصضغط"
BARRIER = "قظصضغط"          # sakin isti'la letter between the kasra and the ra (al-kha' excluded: 344)
AJAMI = ("إبراهيم", "إسرائيل", "إسراءيل", "عمران")
MUKARRAR = ("ضرار", "فرار", "إسرار", "مدرار")
KHULF_RA = ("ذكرا", "سترا", "إمرا", "وزرا", "حجرا", "صهرا")

def vowel(L, j):
    """'f' fatha, 'd' damma, 'k' kasra, 's' sukun, '' none — tanwin counts as its vowel; a bare letter before a final alif is fatha
    (tanwin dropped in this text: كَثِيرا، ذِكْرا)."""
    m = L[j][1]
    if FATHA in m or "ً" in m: return "f"
    if DAMMA in m or "ٌ" in m: return "d"
    if KASRA in m or "ٍ" in m: return "k"
    if SUKUN in m or "ۡ" in m: return "s"
    if j + 1 < len(L) and L[j + 1][0] in "اى" and j + 2 == len(L): return "f"
    return ""

ROOT_BL = ("بكر",)            # initial ب/ل that is a root letter, not a preposition (وَلَا بِكْرٌ)

def prefix_len(b):
    """Length of a separable prefix (و ف + preposition ب ل) whose kasra is not lazima."""
    if re.sub(r"^(و|ف)", "", b) in ROOT_BL: return 0
    m = re.match(r"^(و|ف)?(ب|ل)", b)
    return len(m.group(0)) if m else 0

def ra_rows(w):
    b = bare(w); L = letters(w)
    if any(a in b for a in AJAMI): return []
    out = []
    for j, (ch, m) in enumerate(L):
        if ch != "ر" or vowel(L, j) not in ("f", "d"): continue
        # isti'la after the ra in the same word (an alif between does not shield it): صراط، فراق، إعراض
        k = j + 1
        while k < len(L) and L[k][0] == "ا": k += 1
        if k < len(L) and L[k][0] in ISTILA: continue
        p = j - 1
        if p < 0: continue
        cause = None
        if L[p][0] == "ي" and (vowel(L, p) in ("s", "") ) and p > 0 and vowel(L, p - 1) in ("f", "k"):
            cause = "ya"                                     # خَيْرٌ، بَصِيرٌ
        elif vowel(L, p) == "k":
            if p < prefix_len(b) and L[p][0] in "بل": continue   # kasra of a preposition: بِرَبِّهِمْ
            cause = "kasra"
        elif vowel(L, p) == "s" and p >= 1 and vowel(L, p - 1) == "k" and L[p][0] not in "اوي":
            if L[p][0] in BARRIER: continue                  # مِصْرًا، إِصْرًا
            if p - 1 < prefix_len(b): continue
            cause = "kasra"
        if not cause: continue
        if any(x in b for x in MUKARRAR): continue           # ضِرَارًا: tafkhim for tadil
        out.append("kh" if b in KHULF_RA else "")
    return out[:1]

def lam_rows(w, nxt):
    L = letters(w)
    for j in range(1, len(L)):
        if L[j][0] != "ل" or vowel(L, j) != "f": continue
        p, flag = j - 1, ""
        if L[p][0] == "ا" and p >= 1 and L[p - 1][0] in "صط":
            p, flag = p - 1, "a"                             # طَالَ، فِصَالًا (alif between)
        if L[p][0] not in "صطظ": continue
        v = vowel(L, p)
        if flag != "a" and v not in ("f", "s"): continue
        if flag == "a" and v == "d": continue
        rest = "".join(c for c, _ in L[j + 1:])
        if not flag and rest in ("ى", "ا") and SHADDA in L[j][1] and bare(w).endswith("ى"): flag = "y"   # مُصَلًّى
        elif not flag and j == len(L) - 1: flag = "w"        # يُوصَلَ، فَصَلَ: pause on the lam
        return [flag]
    return []

def detect(vw):
    out = []
    for key, words, i, nxt, _ in words_iter(vw):
        w = words[i]
        for f in ra_rows(w):
            out.append((key, ["ra_warsh", i, f] if f else ["ra_warsh", i]))
        for f in lam_rows(w, nxt):
            out.append((key, ["lam_warsh", i, f] if f else ["lam_warsh", i]))
    return out
