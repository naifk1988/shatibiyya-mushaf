"""باب الهمز المفرد (الشاطبية 214–224).
Rows: ["hamz_sakin", i]        همز ساكن ليس فاءً (عين أو لام): السوسي يبدل
      ["hamz_sakin", i, "f"]   همز ساكن فاءً للكلمة: ورش والسوسي يبدلان
      ["hamz_sakin", i, "b"]   «بئس» حيث وقع: ورش والسوسي
      ["hamz_wawu", i]         همز مفتوح بعد ضم فاءً للكلمة: ورش يبدله واوًا (يُؤَاخِذُ، فَلْيُؤَدِّ)
      ["hamz_liala", i]        «لِئَلَّا»: ورش يبدل الهمزة ياءً
Excluded: «أَنبِئْهُم» (2:33) — sakin for bina' (fi'l amr): Susi reads it with hamza (bayt 218)."""
from common import *

NOT_FA = ("بأس", "رأس", "جئ", "شئ", "خطأ", "ارائت")     # hamza is عين or لام of the word
SUSI_EXCEPT = ("أنبئهم",)

def sakin_hamza(w):
    L = letters(w)
    for k, (ch, m) in enumerate(L):
        if ch in HAMZAS and k > 0 and (SUKUN in m or (not m and k + 1 < len(L) and not (k + 2 == len(L) and L[k + 1][0] == "ا"))):
            return k
    return None

def detect(vw):
    out = []
    for key, words, i, nxt, _ in words_iter(vw):
        w = words[i]; b = bare(w); L = letters(w)
        if "لئلا" in b:
            out.append((key, ["hamz_liala", i])); continue
        k = sakin_hamza(w)
        if k is not None and b not in SUSI_EXCEPT:
            if "بئس" in b: out.append((key, ["hamz_sakin", i, "b"]))
            elif any(x in b for x in NOT_FA): out.append((key, ["hamz_sakin", i]))
            else: out.append((key, ["hamz_sakin", i, "f"]))
            continue
        for k, (ch, m) in enumerate(L):
            if ch == "ؤ" and k > 0 and FATHA in m and DAMMA in L[k - 1][1]:
                out.append((key, ["hamz_wawu", i])); break
    return out
