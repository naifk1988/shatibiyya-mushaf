"""نقل حركة الهمز إلى الساكن قبله لورش (الشاطبية 226–234). Rows: ["naql", i]."""
import re
from common import *
from mim import is_plural_mim

def between(w, nxt):
    if not nxt or not starts_hamza(nxt): return False
    if is_plural_mim(w, nxt): return False
    L = last_letter(w)
    if not L: return False
    a, marks = L[-1]
    if a in HAMZAS and has_tanwin(marks): return True
    if a == "ا" and len(L) >= 2 and "ً" in L[-2][1]: return True
    if a in "اى" or a in HAMZAS: return False
    if has_vowel(marks): return False
    prev = L[-2][1] if len(L) >= 2 else ""
    if a == "و" and SUKUN not in marks and DAMMA in prev: return False
    if a == "ي" and SUKUN not in marks and KASRA in prev: return False
    if a in "وي" and not marks and FATHA not in prev: return False
    return True

def inside(w): return bool(re.match(r"^[وف]?[بكل]?(ال|لل)[أإآءئؤ]", bare(w)))

def detect(vw):
    return [(key, ["naql", i]) for key, words, i, nxt, _ in words_iter(vw) if between(words[i], nxt) or inside(words[i])]
