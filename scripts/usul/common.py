"""Shared helpers for the usul detectors. Words come from data/q4 (the Madinah page data), so indices match the app.
Quirks of this text (learned from audits — keep them in mind in every detector):
- tanwin marks are often dropped before letters of idgham/ikhfa (هُدى، مَثَلا، خَلِيفَة); fatha-tanwin is written with alif (هُودًا);
  before ب tanwin may appear as a single vowel (كَاتِبُ بِالْعَدْلِ = كاتبٌ).
- the sukun of a final nun/mim may be dropped before an assimilated letter (مِنْهُم مَّن، مِن رَّبِّهِمْ).
- alif maqsura before a pronoun is written ى inside the word (هُدَىهُمْ، اشْتَرَىهُ); some words keep a plain alif (الدُّنْيَا، سِيمَاهُمْ، الرِّبَوااْ).
- silent alif after plural waw is written «اْ» (قَالُواْ); ZWJ (U+200D) and tatweel (U+0640) occur inside words (إِبْرَاهِ‍يمَ، الْـئَانَ).
- hamza forms: أ إ آ ء ؤ ئ, and «ءَا» for initial alif-madda (ءَامَنُواْ)."""
import json, glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SURAHS = (1, 2)
FATHA, DAMMA, KASRA = "َ", "ُ", "ِ"
HARAKA = FATHA + DAMMA + KASRA
TANWIN = "ًٌٍ"
SUKUN, SHADDA = "ْ", "ّ"
MARKS = re.compile(r"[ً-ٰٟۜ-ۭ]")
HAMZAS = "أإآءؤئ"
HAMZA_START = "أإآء"

def clean(w): return w.replace("‍", "").replace("ـ", "")
def bare(w): return MARKS.sub("", clean(w))

def letters(w):
    """[[letter, marks]] — marks are the diacritics written after the letter."""
    out = []
    for ch in clean(w):
        if MARKS.match(ch):
            if out: out[-1][1] += ch
        else:
            out.append([ch, ""])
    return out

def last_letter(w):
    """Letters without the silent alif written after a plural waw (قَالُواْ)."""
    L = letters(w)
    if len(L) >= 2 and L[-1][0] == "ا" and L[-2][0] == "و" and L[-1][1] in ("", SUKUN):
        L = L[:-1]
    return L

def starts_hamza(w): b = bare(w); return bool(b) and b[0] in HAMZA_START
def starts_wasl(w): b = bare(w); return bool(b) and b[0] in "اٱ"
def has_vowel(marks): return any(c in marks for c in HARAKA) and not any(c in marks for c in TANWIN)
def has_tanwin(marks): return any(c in marks for c in TANWIN)
def moving(marks): return has_vowel(marks) and SHADDA not in marks

def load_vw():
    vw = {}
    for f in glob.glob(os.path.join(ROOT, "data", "q4", "*.json")):
        vw.update(json.load(open(f, encoding="utf-8"))["vw"])
    return vw

def ayahs(vw):
    """Yield (key, words, next_ayah_words_or_None) for al-Fatiha and al-Baqarah in order."""
    for s in SURAHS:
        n = 1
        while f"{s}:{n}" in vw:
            yield f"{s}:{n}", vw[f"{s}:{n}"], vw.get(f"{s}:{n+1}")
            n += 1

def words_iter(vw):
    """Yield (key, words, i, nxt, nxt_cross): nxt = next word in the ayah or None; nxt_cross also crosses into the next ayah."""
    for key, words, nexta in ayahs(vw):
        for i in range(len(words)):
            nxt = words[i + 1] if i + 1 < len(words) else None
            yield key, words, i, nxt, (nxt if nxt is not None else (nexta[0] if nexta else None))
