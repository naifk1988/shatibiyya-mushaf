"""الإدغام الكبير للسوسي (الشاطبية 116–157): المثلان (116–131) والمتقاربان في كلمة وفي كلمتين (132–157).
Rows: ["idgham", i, flag]. Flags:
  ""/"x"/"v"  المثلان (x: قبله ساكن صحيح فالإخفاء، v: بين آيتين)
  "q"/"qx"/"qv" المتقاربان في كلمتين (qx: قبله ساكن صحيح فالإخفاء، qv: بين آيتين)
  "qw" القاف في الكاف في كلمة (خلقكم)، "m" الميم قبل الباء (تسكن فتخفى)، "qk" وجهان (وآتوا الزكاة ثم)."""
import os
from common import *

def _hafs():
    """Fully marked Hafs text (same word count per ayah as data/q4): used only as an oracle for tanwin and sukun, never for indexing."""
    H = {}
    for l in open(os.path.join(ROOT, "data", "raw", "hafs_1_2.txt"), encoding="utf-8"):
        if " " in l:
            k, t = l.strip().split(" ", 1); H[k] = t.split()
    return H
HAFS = _hafs()

def hafs_word(key, i):
    ws = HAFS.get(key)
    return ws[i] if ws and i < len(ws) else ""

def tanwin_at(key, i):
    """True if the Hafs word ends with tanwin (q4 drops it before idgham/ikhfa letters and writes it as a single haraka before ب)."""
    L = letters(hafs_word(key, i))
    while L and L[-1][0] in "اى" and not L[-1][1]: L = L[:-1]
    return bool(L) and has_tanwin(L[-1][1])

def first(w): b = bare(w); return b[:1]

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

def _sakin(p):
    """Letter p is sakin: sukun, or a madd letter without a vowel (ا، ى، و، ي)."""
    return SUKUN in p[1] or (p[0] in "اىوي" and not any(c in p[1] for c in HARAKA + SHADDA))

def _sahih_sakin(p): return SUKUN in p[1] and p[0] not in "اىوي"

# الحرف الأول ← الحروف التي يدغم فيها (البيت 139–153)
DAL = set("تسذشضثزصظج")
TA = set("ثسذشضزصظجط")
THA = set("تسذشض")

def mutaqaribayn(w, nxt, key, i):
    """Return flag "q"/"qx"/"m"/"qk" if the last letter of w is assimilated by al-Susi into the first letter of nxt, else None."""
    L = last_letter(w)
    if not L or not nxt or len(L) < 2: return None
    a, marks = L[-1]
    if a == "ة": a = "ت"
    b = first(nxt)
    if not b or a == b: return None
    if not moving(marks) or tanwin_at(key, i): return None          # المانع: المنوّن والمشدّد والساكن
    bw, bn, p = bare(w), bare(nxt), L[-2]
    sak, sah = _sakin(p), _sahih_sakin(p)
    ok, flag = False, None
    if a == "ح": ok = b == "ع" and bw.endswith("زحزح")
    elif a == "ق": ok = b == "ك" and not sak
    elif a == "ك": ok = b == "ق" and not sak
    elif a == "ج": ok = (b == "ت" and bw.endswith("المعارج") and bn.startswith("تعرج")) or (b == "ش" and bw.endswith("أخرج") and bn.startswith("شطأ"))
    elif a == "ش": ok = b == "س" and bw.endswith("العرش") and bn.startswith("سبيل")
    elif a == "ض": ok = b == "ش" and bw.endswith("بعض") and bn.startswith("شأن")
    elif a == "س": ok = (b == "ز" and bw.endswith("النفوس")) or (b == "ش" and bw.endswith("الرأس") and bn.startswith("شيب"))
    elif a == "د": ok = b in DAL and not (FATHA in marks and sak and b != "ت")
    elif a == "ت":
        if b in TA:
            if letters(w)[-1][0] == "ت" and (FATHA in marks or DAMMA in marks): return None   # تاء الخطاب والمتكلم
            ok = True
            if FATHA in marks and p[0] == "ا": flag = "qk"           # المفتوحة بعد ألف: حُمِّلوا التوراة، وآتوا الزكاة ثم … بوجهين
    elif a == "ث": ok = b in THA
    elif a == "ذ": ok = (b == "س" and bw.endswith("اتخذ") and bn.startswith("سبيل")) or (b == "ص" and bw.endswith("اتخذ") and bn.startswith("صاحب"))
    elif a == "ر": ok = b == "ل" and not (FATHA in marks and sak)
    elif a == "ل": ok = b == "ر" and (not (FATHA in marks and sak) or bw in ("قال", "وقال", "فقال"))
    elif a == "ن": ok = b in "رل" and (not sak or (b == "ل" and bw in ("نحن", "ونحن", "فنحن")))
    elif a == "م": ok = b == "ب" and not sak; flag = "m" if ok else None
    elif a == "ب": ok = b == "م" and bw.endswith("يعذب") and bn == "من"
    if not ok: return None
    return flag or ("qx" if sah else "q")

# ولم يؤت سعة (البقرة 247) مجزوم: إظهار. فيغفر لمن / ويعذب من (البقرة 284) يقرؤهما أبو عمرو بالجزم فهما من الإدغام الصغير (idgham_saghir).
SKIP = {("2:247", "يؤت"), ("2:284", "فيغفر"), ("2:284", "ويعذب")}

def one_word(w):
    """القاف في الكاف في كلمة: قبل القاف متحرك وبعد الكاف ميم جمع (خلقكم، يرزقكم)؛ ميثاقكم ونرزقك بالإظهار."""
    L = letters(w)
    for j in range(1, len(L) - 2):
        if L[j][0] == "ق" and L[j + 1][0] == "ك" and L[j + 2][0] == "م" and moving(L[j][1]) and not _sakin(L[j - 1]):
            return True
    return False

def detect(vw):
    out = []
    for key, words, i, nxt, nxc in words_iter(vw):
        w = words[i]
        if (key, bare(w)) in SKIP: continue
        r = mithlayn(w, nxc)
        if r is not None:
            if nxt is None and not r: r = "v"
            out.append((key, ["idgham", i, r] if r else ["idgham", i]))
            continue
        if bare(w) == "مناسككم": out.append((key, ["idgham", i])); continue
        if one_word(w): out.append((key, ["idgham", i, "qw"])); continue
        q = mutaqaribayn(w, nxc, key, i)
        if q is not None:
            if nxt is None and q == "q": q = "qv"
            out.append((key, ["idgham", i, q]))
    return out
