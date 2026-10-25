#!/usr/bin/env python3
"""Find the places of four usul rules in al-Fatiha and al-Baqarah, from the words of the Madinah page data (data/q4),
so that word indices match what the app shows. Conditions and exceptions follow data/usul_rules.json (from al-Wafi).
Output: data/u/<surah>.json  {"s:a": [[rule, wordIndex, flag], ...]}
  flags: mim  "h" = before hamzat qat' (Warsh too)          idgham "x" = sakin before the merged letter (ikhfa/ikhtilas), "v" = across two ayahs (wasl only)
         imala "w" = only when pausing   "k" = al-Kisa'i only   "dk" = al-Duri 'an al-Kisa'i only
Run: python3 scripts/build_usul.py            (add --list to print every place for review)"""
import json, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SURAHS = (1, 2)
HARAKA = "َُِ"            # fatha damma kasra
TANWIN = "ًٌٍ"
SUKUN, SHADDA = "ْ", "ّ"
MARKS = re.compile(r"[ً-ٰٟۜ-ۭ]")
HAMZA_START = "أإآء"

def clean(w): return w.replace("\u200d", "").replace("\u0640", "")   # zero-width joiner and tatweel used in the page text
def bare(w): return MARKS.sub("", clean(w))

def letters(w):
    """[(letter, marks)] — marks are the diacritics written after the letter."""
    out = []
    for ch in clean(w):
        if MARKS.match(ch):
            if out: out[-1][1] += ch
        else:
            out.append([ch, ""])
    return out

def last_letter(w):
    """The final pronounced letter: drop the silent alif written after a plural waw (قَالُواْ)."""
    L = letters(w)
    if len(L) >= 2 and L[-1][0] == "ا" and L[-2][0] == "و" and (L[-1][1] in ("", SUKUN)):
        L = L[:-1]
    return L

def starts_hamza(w):
    b = bare(w)
    return bool(b) and b[0] in HAMZA_START

def starts_wasl(w):
    b = bare(w)
    return bool(b) and b[0] in "اٱ"

def moving(marks): return any(c in marks for c in HARAKA) and not any(c in marks for c in TANWIN) and SHADDA not in marks

# ---------- 1. صلة ميم الجمع ----------
def mim(words, i, nxt):
    b = bare(words[i])
    L = letters(words[i])
    if not nxt or not L or L[-1][0] != "م" or (L[-1][1] and SUKUN not in L[-1][1]): return None   # sukun, or no mark (dropped before an assimilated letter)
    if not re.search(r"(هم|كم|تم)$", b): return None
    if b in ("ثم", "لم", "أم", "يوم", "كم", "وكم", "فكم"): return None   # كم is the particle, not a plural mim
    if starts_wasl(nxt): return None
    return "h" if starts_hamza(nxt) else ""

# ---------- 2. الإدغام الكبير للسوسي: المثلان ----------
def idgham(words, i, nxt):
    if not nxt: return None
    L = last_letter(words[i])
    if not L: return None
    a, marks = L[-1]
    if a == "ة": a = "ت"
    if not moving(marks): return None              # sakin, tanwin, shadda, madd letter, or tanwin dropped from the text
    b0 = bare(nxt)[:1]
    if a != b0: return None
    # before ب this text writes tanwin as a single vowel (كَاتِبُ بِالْعَدْلِ = كاتبٌ): a damma/kasra on a word without ال may be tanwin
    if a == "ب" and not bare(words[i]).startswith(("ال", "وال", "فال", "بال")) and ("\u064F" in marks or "\u0650" in marks): return None
    if a == "ت" and letters(words[i])[-1][0] == "ت": return None   # تاء المتكلم/المخاطب (كنتُ ترابا، أنتَ تكره)
    prev = L[-2] if len(L) >= 2 else None
    return "x" if prev and SUKUN in prev[1] and prev[0] not in "اوي" else ""

# ---------- 3. النقل لورش ----------
MADD = "اى"
def naql_between(words, i, nxt):
    if not nxt or not starts_hamza(nxt): return None
    if mim(words, i, nxt) is not None: return None   # Warsh joins the plural mim instead
    L = last_letter(words[i])
    if not L: return None
    a, marks = L[-1]
    if a in "أإآءؤئ" and any(c in marks for c in TANWIN): return ""   # hamza carrying tanwin (وَأَدَاءٌ إِلَيْهِ)
    if a == "ا" and len(L) >= 2 and "\u064B" in L[-2][1]: return ""   # fatha-tanwin written with alif (هُودًا أَوْ)
    if a in MADD or a in "أإآءؤئ": return None
    if any(c in marks for c in HARAKA) and not any(c in marks for c in TANWIN): return None   # a voweled letter (shadda or not)
    prev = L[-2][1] if len(L) >= 2 else ""
    if a == "و" and SUKUN not in marks and "ُ" in prev: return None   # long u
    if a == "ي" and SUKUN not in marks and "ِ" in prev: return None   # long i
    if a in "وي" and not marks and "َ" not in prev: return None
    return ""

def naql_inside(w):
    return bool(re.match(r"^[وف]?[بكل]?(ال|لل)[أإآءئؤ]", bare(w)))

# ---------- 4. الإمالة الكبرى لحمزة والكسائي ----------
NOT_IMALA = {"على", "إلى", "حتى", "لدى"}
PREFIX = re.compile(r"^(و|ف)")
# written with alif in this text, imala'd (from the rule card): base form → flag
ALIF_WORDS = {"الدنيا": "", "والدنيا": "", "بالدنيا": "", "الربا": "", "الربواا": "", "والربواا": "", "بسيماهم": "", "سيماهم": "",
              "خطاياكم": "k", "مرضات": "k", "مرضاة": "k", "فأحياكم": "k", "أحياكم": "k", "فأحيا": "k", "أحياهم": "k", "هداي": "dk"}

def imala(words, i, nxt):
    b = bare(words[i])
    if b in ALIF_WORDS: return ALIF_WORDS[b]
    if re.search(r"ى(ه|هم|هما|هن|ها|ك|كم|نا|ني)$", b): return ""      # هُدَىهُمْ، اشْتَرَىهُ: a pronoun does not block imala
    if not b.endswith("ى"): return None
    if b in NOT_IMALA or PREFIX.sub("", b) in NOT_IMALA: return None
    L = letters(words[i])
    before = L[-2][1] if len(L) >= 2 else ""
    if "\u064E" not in before or nxt is not None and starts_wasl(nxt): return "w"   # tanwin (its sign is dropped in this text) or a sakin follows
    return ""

def main():
    vw = {}
    for f in glob.glob(os.path.join(ROOT, "data", "q4", "*.json")):
        vw.update(json.load(open(f, encoding="utf-8"))["vw"])
    out = {s: {} for s in SURAHS}
    for s in SURAHS:
        n = 1
        while f"{s}:{n}" in vw:
            key = f"{s}:{n}"; words = vw[key]; nextkey = f"{s}:{n+1}"
            rows = []
            for i, w in enumerate(words):
                nxt = words[i + 1] if i + 1 < len(words) else None
                nxt_x = nxt if nxt is not None else (vw[nextkey][0] if nextkey in vw else None)   # idgham crosses ayah ends in wasl
                for rule, fn, nx in (("mim", mim, nxt), ("idgham", idgham, nxt_x), ("imala", imala, nxt)):
                    r = fn(words, i, nx)
                    if r is not None and rule == "idgham" and nxt is None and not r: r = "v"   # across two ayahs: only when reading on
                    if r is not None: rows.append([rule, i, r] if r else [rule, i])
                r = naql_between(words, i, nxt)
                if r is not None or naql_inside(w): rows.append(["naql", i])
            if "مناسككم" in [bare(x) for x in words]:
                rows.append(["idgham", [bare(x) for x in words].index("مناسككم")])
            if rows: out[s][key] = rows
            n += 1
    os.makedirs(os.path.join(ROOT, "data", "u"), exist_ok=True)
    tot = {}
    for s, d in out.items():
        json.dump(d, open(os.path.join(ROOT, "data", "u", f"{s}.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
        for rows in d.values():
            for r in rows: tot[r[0]] = tot.get(r[0], 0) + 1
    print("places:", tot)
    if "--list" in sys.argv:
        for s, d in out.items():
            for key, rows in d.items():
                ws = vw[key]
                for r in rows:
                    nx = ws[r[1] + 1] if r[1] + 1 < len(ws) else "⟂"
                    print(key, r[0], (r[2] if len(r) > 2 else ""), ws[r[1]], "→", nx)

if __name__ == "__main__":
    main()
