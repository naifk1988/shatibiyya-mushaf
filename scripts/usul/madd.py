"""باب المد والقصر (الشاطبية 168–181) — al-Fatiha and al-Baqarah.
Rules:
  madd_muttasil  ["madd_muttasil", i, flag?]  madd letter + hamza in one word (flags: nabi, mikal = farsh words read with hamza by others)
  madd_munfasil  ["madd_munfasil", i, flag?]  word ending in a madd letter, next word starts with hamzat qat'
                 flags: m (plural-mim sila), h (sila of ha al-kinaya after a moving letter), n (يا النداء), t (ها التنبيه),
                        ana (أنا أحيي), y1/y2/y3 (ya al-idafa), z1/z2 (ya'at zawa'id kept in wasl)
  madd_badal     ["madd_badal", i, flag?]     madd letter after hamza (Warsh); flag f = Nafi''s hamzated farsh words
  madd_lin       ["madd_lin", i]              ي/و sakin after fatha before hamza in one word (Warsh)
Madd lazim (agreed by all) is not marked."""
import re
from common import *
from mim import is_plural_mim

ALLAH = {"الله", "لله", "بالله", "فالله", "والله", "تالله", "ولله", "فلله", "ءالله"}

def is_madd(L, j):
    """Is letter j of L a madd letter (alif, or و after damma / ي after kasra with no vowel, sukun or shadda)?"""
    a, m = L[j]
    prev = L[j - 1][1] if j > 0 else ""
    if a == "ا":
        return j > 0 and FATHA in prev and not has_tanwin(prev) and SUKUN not in m
    if a == "ى":
        return j > 0 and FATHA in prev and not has_tanwin(prev) and not has_tanwin(m)
    if a == "و":
        return j > 0 and DAMMA in prev and not has_tanwin(prev) and not m
    if a == "ي":
        return j > 0 and KASRA in prev and not has_tanwin(prev) and not m
    return False

# ---------- المتصل ----------
FARSH_MUTTASIL = {("2:61", "النبيين"): "nabi", ("2:177", "والنبيين"): "nabi", ("2:213", "النبيين"): "nabi",
                  ("2:136", "النبيون"): "nabi", ("2:246", "لنبي"): "nabi", ("2:247", "نبيهم"): "nabi",
                  ("2:248", "نبيهم"): "nabi", ("2:98", "وميكىل"): "mikal"}

def nida_prefix(w):
    """Length (in letters) of a joined يا/ها prefix when it is directly followed by a hamza (يَاأَيُّهَا، يَاـئَادَمُ، هَاؤُلَاءِ)."""
    b = bare(w)
    if re.match(r"^[وف]?(يا|ها)[أإآءؤئ]", b):
        return b.index("ا") + 1
    return 0

def muttasil(w):
    b = bare(w)
    if b in ("فادارائتم",): return False          # فَادَّارَأْتُمْ: the alif carries no madd (hamza sakin)
    if "أولئك" in b: return True                   # أُولَٰٓئِكَ: the alif (dagger alif in the Uthmani script) is dropped in this text
    L = letters(w); start = nida_prefix(w)
    for j in range(max(1, start), len(L) - 1):
        if is_madd(L, j) and L[j + 1][0] in HAMZAS:
            return True
    return False

# ---------- المنفصل ----------
YA_IDAFA = {("2:30", "إني"): "y1", ("2:33", "إني"): "y1", ("2:152", "فاذكروني"): "y2", ("2:249", "مني"): "y3"}
ZAWAID = {("2:186", "الداع"): "z1", ("2:197", "واتقون"): "z2"}

def ends_madd(w):
    b = bare(w)
    if b.endswith("ربواا") or b == "يستحي": return True   # الرِّبَوٰٓا۟ / يَسْتَحْيِۦٓ (dropped dagger alif / small ya in this text)
    L = last_letter(w)
    if len(L) >= 2 and L[-1][0] == "ا" and SUKUN in L[-1][1]: L = L[:-1]   # الرِّبَوااْ
    return len(L) >= 2 and is_madd(L, len(L) - 1)

def ha_sila(w):
    """Ha al-kinaya after a moving letter (its sila is read by all): بِهِ، لَهُ، أَمْرُهُ."""
    b = bare(w); L = letters(w)
    if len(L) < 2 or L[-1][0] != "ه" or not has_vowel(L[-1][1]) or FATHA in L[-1][1]: return False
    if b in ALLAH or b.endswith("اله") or b.endswith("لاه"): return False
    return has_vowel(L[-2][1])

def munfasil(key, w, nxt):
    """Return None or the flag ('' for the general case)."""
    b = bare(w)
    if (key, b) in ZAWAID: return ZAWAID[(key, b)]
    if not nxt or not starts_hamza(nxt): return None
    if (key, b) in YA_IDAFA: return YA_IDAFA[(key, b)]
    if b == "أنا": return "ana"
    if is_plural_mim(w, nxt): return "m"
    if ha_sila(w): return "h"
    if ends_madd(w): return ""
    return None

# ---------- البدل ----------
BADAL_SKIP = ("إسراءيل", "إسرائيل", "يؤاخذ", "تؤاخذ", "الصابئين", "والصابئين")
FARSH_BADAL = {("2:61", "النبيين"), ("2:177", "والنبيين"), ("2:213", "النبيين"), ("2:136", "النبيون"),
               ("2:81", "خطيئته")}

def badal(w):
    b = bare(w)
    if any(s in b for s in BADAL_SKIP) or b == "فادارائتم": return False
    L = letters(w)
    for j, (a, m) in enumerate(L[:-1]):
        if a not in "أإءئؤ": continue
        if j > 0 and SUKUN in L[j - 1][1] and L[j - 1][0] not in "اويى":
            # hamza after a sound sakin in the same word (القرآن، مسئولا) — but the lam of ال (الآخرة) is naql, not excluded
            if not (L[j - 1][0] == "ل" and j >= 2 and L[j - 2][0] in "اٱ"): continue
        nx, nm = L[j + 1]
        if j + 2 < len(L) and L[j + 2][0] in HAMZAS: continue   # a hamza after the madd letter makes it muttasil, the stronger madd (رِئَاءَ)
        if not m and (nx not in "اىوي" or has_vowel(nm)):            # الْأخِرَةِ، الْأيَاتِ، لِأدَمَ = hamza + alif (ءا) dropped in this text
            return True
        if FATHA in m and not has_tanwin(m) and nx in "اى" and SUKUN not in nm and not has_tanwin(nm):
            if j + 2 < len(L) or nx == "ا":
                return True
        if DAMMA in m and nx == "و" and not nm: return True
        if KASRA in m and nx == "ي" and not nm: return True
    return False

# ---------- اللين المهموز ----------
def lin(w):
    L = letters(w)
    for j in range(1, len(L) - 1):
        a, m = L[j]
        if a in "وي" and SUKUN in m and FATHA in L[j - 1][1] and L[j + 1][0] in HAMZAS:
            return True
    return False

def detect(vw):
    out = []
    for key, words, i, nxt, _ in words_iter(vw):
        w = words[i]; b = bare(w)
        if (key, b) in FARSH_MUTTASIL:
            out.append((key, ["madd_muttasil", i, FARSH_MUTTASIL[(key, b)]]))
        elif muttasil(w):
            out.append((key, ["madd_muttasil", i]))
        np = nida_prefix(w)
        if np:
            out.append((key, ["madd_munfasil", i, "t" if bare(w)[np - 2] == "ه" else "n"]))
        f = munfasil(key, w, nxt)
        if f is not None:
            out.append((key, ["madd_munfasil", i, f] if f else ["madd_munfasil", i]))
        if (key, b) in FARSH_BADAL:
            out.append((key, ["madd_badal", i, "f"]))
        elif badal(w):
            out.append((key, ["madd_badal", i]))
        if lin(w):
            out.append((key, ["madd_lin", i]))
    return out
