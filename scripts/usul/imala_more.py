"""Other chapters of «باب الفتح والإمالة» and the next chapter, for al-Fatiha + al-Baqarah:
- imala_ra     (321–326, 332–334) alif before a final ra with an original kasra; flags: "kf" كافرين بالياء, "h" حمارك (+ Ibn Dhakwan khulf)
- imala_af3al  (318–320) the ten verbs for Hamza / Ibn Dhakwan; flags: "jd" جاء/شاء (+ Ibn Dhakwan), "z1" فزادهم (first زاد, + Ibn Dhakwan), "z" other زاد (+ Ibn Dhakwan khulf)
- imala_ha     (339–342) al-Kisa'i's imala of ha' al-ta'nith and the letter before it in pause; flags: "akh" one of أكهر after ya sakina or kasra, "t" written with open ta
- imala_alfaz  (327–331) single words: "nas" الناس مجرورًا (al-Duri 'an Abi Amr), "dk" بارئكم، آذانهم، طغيانهم (al-Duri 'an al-Kisa'i)"""
import re
from common import *

PRON = r"(ه|هم|هما|هن|ها|ك|كم|نا|ني|كما)$"

def imala_ra(w):
    b = bare(w)
    if re.match(r"^(و|ف|ب|ل)?(ال|لل)?كافرين$", b): return "kf"
    L = letters(w)
    for j in range(len(L) - 1, 0, -1):
        if L[j][0] == "ر" and L[j - 1][0] == "ا":
            rest = "".join(x[0] for x in L[j + 1:])
            if rest and not re.fullmatch(PRON[:-1], rest): return None   # ra not final
            if rest in ("ي", "ني"): return None                             # أنصاري: kasra for the ya, not original
            m = L[j][1]
            if SHADDA in m: return None                                    # مضارّ، بضارّين: the ra is doubled
            if KASRA in m or "ٍ" in m: return "h" if b.endswith("حمارك") else ""
            return None
    return None

VERB = re.compile(r"^(و|ف)?(جاء|شاء|زاد|خاب|خاف|طاب|ضاق|حاق|زاغ|ران)(ت|تا|و|وا|ك|كم|كما|ه|ها|هم|هما|هن|نا|تك|تكم|ته|تها|تهم|ني)?$")
def imala_af3al(w, first_zad):
    m = VERB.match(bare(w))
    if not m: return None
    v, suf = m.group(2), m.group(3) or ""
    if v == "زاغ" and suf.startswith("ت"): return None                  # زاغت: Hamza opens it
    if v in ("جاء", "شاء"): return "jd"
    if v == "زاد": return "z1" if first_zad else "z"
    return ""

NEVER = set("حقضغاطعصخظ")       # حق ضغاط عص خظا
AKHAR = set("ءأإئؤكهر")          # أكهر (any hamza form)
def imala_ha(w):
    L = letters(w)
    b = bare(w)
    if b in ("رحمت", "نعمت"): return "t"                                  # written with ta, al-Kisa'i stops with ha
    if len(L) < 2 or L[-1][0] != "ة": return None
    p = L[-2][0]
    if p in NEVER: return None
    if p not in AKHAR: return ""
    k = len(L) - 3
    while k >= 0 and L[k][0] == "ا" and SUKUN in L[k][1]: k -= 1          # silent alif in مِاْئَة
    if k < 0: return None
    c, mk = L[k]
    if KASRA in mk: return "akh"
    if c == "ي" and not any(x in mk for x in FATHA + DAMMA): return "akh"  # ya sakina (lin or madd)
    if SUKUN in mk and k >= 1 and KASRA in L[k - 1][1]: return "akh"        # لعبرة، وجهة: the sakin does not bar
    return None

def imala_alfaz(w):
    b = bare(w)
    if re.match(r"^(و|ف|ب|ل)?(ال|لل)ناس$", b) and KASRA in letters(w)[-1][1]: return "nas"
    if re.match(r"^(و|ف)?(بارئكم|ءاذانهم|طغيانهم)$", b): return "dk"
    return None

def detect(vw):
    out = []
    first_zad = True
    for key, words, i, nxt, _ in words_iter(vw):
        w = words[i]
        for rid, fn in (("imala_ra", imala_ra), ("imala_ha", imala_ha), ("imala_alfaz", imala_alfaz)):
            r = fn(w)
            if r is not None: out.append((key, [rid, i, r] if r else [rid, i]))
        r = imala_af3al(w, first_zad)
        if r is not None:
            if r == "z1": first_zad = False
            out.append((key, ["imala_af3al", i, r] if r else ["imala_af3al", i]))
    return out
