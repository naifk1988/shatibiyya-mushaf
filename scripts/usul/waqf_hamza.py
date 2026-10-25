"""وقف حمزة وهشام على الهمز (الشاطبية 235–254) — التخفيف القياسي فقط. Rows: ["waqf_hamza", i, flag].
Flags (hamza position in the word as written in data/q4):
  s  ساكن متوسط بعد متحرك → إبدال حرف مد (حمزة)
  f  متطرف بعد متحرك (يُسكَّن للوقف) → إبدال حرف مد (حمزة وهشام)
  a  متطرف بعد ألف → إبدال ألفًا مع القصر والتوسط والمد (حمزة وهشام)
  am متوسط بعد ألف → تسهيل بين بين مع المد والقصر (حمزة)
  nm / nf  متحرك بعد ساكن صحيح أو حرف لين أو مد أصلي → نقل (متوسط: حمزة؛ متطرف: حمزة وهشام)
  dm / df  بعد ياء أو واو زائدة → إبدال وإدغام (متوسط: حمزة؛ متطرف: حمزة وهشام)
  y  مفتوح بعد كسر → ياء؛  w  مفتوح بعد ضم → واو (حمزة)
  t  سائر المتحرك بعد متحرك (متوسط) → تسهيل بين بين (حمزة)
  combined flags join two of these with "_" (e.g. "s_a" in «الْبَأْسَاءِ»).
Not marked (described in the card): initial hamza; hamza made medial by a separable prefix (و ف ب ل ك س يا ها ء الاستفهام ال،
and «الذي اؤتمن») which has two faces (تحقيق وتخفيف)."""
import re
from common import *

ZAID_PREFIX = re.compile(r"^((و|ف)?(ل|ب|ك|س)?(ال|يا|ها|ء|أ)?|ا)$")
ROOT_INITIAL = ("بئس", "سأل", "سئل", "فئة")             # the letter before the hamza belongs to the word
ZAID_LETTER = ("خطيئته", "قروء")                       # ياء/واو زائدة قبل الهمز (فعيلة، فعول)
TANWIN_FATH = {("2:22", 6), ("2:22", 10), ("2:171", 10), ("2:171", 11)}   # «بِنَاءً»، «مَاءً»، «دُعَاءً وَنِدَاءً» (tanwin dropped in q4)

def positions(w, key=None, i=None):
    """[(k, flag)] for each hamza in the word that Hamza changes in the qiyasi way."""
    L = letters(w)
    b = bare(w)
    out = []
    for k, (ch, m) in enumerate(L):
        if ch not in HAMZAS or k == 0: continue
        j = k - 1
        if L[j][0] == "ا" and SUKUN in L[j][1] and j > 0: j -= 1      # silent alif: «مِاْئَةَ»
        pre = "".join(c for c, _ in L[:k])
        if ZAID_PREFIX.match(pre) and not any(r in b for r in ROOT_INITIAL): continue
        p, pm = L[j]
        rest = L[k + 1:]
        final = not rest
        if not rest and (key, i) in TANWIN_FATH: final = False
        if len(rest) == 1 and rest[0][0] == "ا": final = False                         # «شَيْئا»، «جُزْءا»: alif of tanwin
        zaid = any(z in b for z in ZAID_LETTER)
        tanwin_alif = len(rest) == 1 and rest[0][0] == "ا"
        sakin = SUKUN in m or (not m and "ارائت" in b)      # «فَادَّارَائتُمْ»؛ «جُزْءا» = جزءًا
        p_alif = p == "ا" and not pm
        p_sakin = (SUKUN in pm) or (p in "وي" and not pm)
        if sakin: f = "s"
        elif p_alif: f = "a" if final else "am"
        elif p_sakin: f = ("df" if final else "dm") if zaid else ("nf" if final else "nm")
        elif final: f = "f"
        elif FATHA in m and KASRA in pm: f = "y"
        elif FATHA in m and DAMMA in pm: f = "w"
        else: f = "t"
        out.append((k, f))
    return out

def detect(vw):
    out = []
    for key, words, i, nxt, _ in words_iter(vw):
        ps = positions(words[i], key, i)
        if ps:
            out.append((key, ["waqf_hamza", i, "_".join(f for _, f in ps)]))
    return out
