"""الهمزتان من كلمة (الشاطبية 183–201) ومن كلمتين (202–213).
Rows: ["hamzatayn_kalima", i] — the word containing two adjacent hamzas (first مفتوحة; in al-Baqarah both are مفتوحتان);
      ["hamzatayn_kalimatayn", i, flag] — i is the FIRST word of the pair (ends in a hamza, next word starts with hamzat qat').
Flags (first+second vowel): ks مكسورتان (متفقتان); fk مفتوحة/مكسورة; df مضمومة/مفتوحة; kf مكسورة/مفتوحة; dk مضمومة/مكسورة;
plus ff/dd/fd for completeness (not in al-Fatiha/al-Baqarah). Pairs across an ayah end are skipped (the reader stops: tahqiq for all)."""
from common import *

def two_in_word(w):
    """Two hamzas in a row at the start of the word: ءَأَ / أَأَ / أَإِ / أَؤُ (ءَا of ءَامَنُواْ is one hamza + alif)."""
    L = letters(w)
    for k in range(min(len(L) - 1, 3)):
        if L[k][0] in HAMZAS and L[k + 1][0] in HAMZAS and FATHA in L[k][1]:
            return True
    return False

def vowel(marks):
    for c, v in ((FATHA, "f"), (DAMMA, "d"), (KASRA, "k")):
        if c in marks: return v
    return None

def pair(w, nxt):
    """Flag for a word ending in a voweled hamza (no tanwin) followed by a word starting with hamzat qat'."""
    if not nxt or not starts_hamza(nxt): return None
    L = letters(w)
    if not L or L[-1][0] not in HAMZAS or has_tanwin(L[-1][1]): return None
    v1 = vowel(L[-1][1])
    N = letters(nxt)
    v2 = vowel(N[0][1]) if N[0][0] != "آ" else "f"
    if N[0][0] == "ء" and len(N) > 1 and N[1][0] == "ا": v2 = "f"
    if not v1 or not v2: return None
    return {"ff": "ff", "kk": "ks", "dd": "dd"}.get(v1 + v2, v1 + v2)

def detect(vw):
    out = []
    for key, words, i, nxt, _ in words_iter(vw):
        w = words[i]
        if two_in_word(w):
            out.append((key, ["hamzatayn_kalima", i]))
        f = pair(w, nxt)
        if f:
            out.append((key, ["hamzatayn_kalimatayn", i, f]))
    return out
