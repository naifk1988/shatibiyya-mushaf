"""الإدغام الصغير (الشاطبية 255–290) في الفاتحة والبقرة. Rows: [rule, i, flag]; the flag names the following letter or the word.
  idh_dhal   ذال إذ (259–261)        flags: t z sad d sin j
  qad_dal    دال قد (262–265)        flags: sin dh dad za z j sad sh
  ta_tanith  تاء التأنيث (266–269)   flags: sin th sad z za j
  hal_bal    لام هل وبل (270–273)    flags: t th za z sin n ta dad
  qarubat    حروف قربت مخارجها (277–285): yf (يفعل ذلك) r (الراء المجزومة في اللام) rv (بوصل الآيتين) gh (فيغفر لمن، البقرة 284)
             lb (لبثت) akh (اتخذتم/أخذتم) yu (يعذب من، البقرة 284) bf (الباء المجزومة في الفاء)
  nun_sakina النون الساكنة والتنوين (286–290): خلف عن حمزة في الواو والياء؛ flags: w y wv yv (v: بوصل الآيتين)"""
from common import *
from idgham import hafs_word, tanwin_at

LETTER = {"ت": "t", "ث": "th", "ج": "j", "د": "d", "ذ": "dh", "ز": "z", "س": "sin", "ش": "sh", "ص": "sad", "ض": "dad", "ط": "ta", "ظ": "za", "ن": "n"}
IDH = "تزصدسج"
QAD = "سذضظزجصش"
TA = "سثصزظج"
HALBAL = "تثظزسنطض"

def final_sakin(key, i):
    """Last letter carries sukun in the fully marked Hafs text (q4 often drops it before an assimilated letter)."""
    L = letters(hafs_word(key, i))
    return bool(L) and SUKUN in L[-1][1]

def detect(vw):
    out = []
    for key, words, i, nxt, nxc in words_iter(vw):
        w, b = words[i], bare(words[i])
        n1 = bare(nxt)[:1] if nxt else ""
        if nxt:
            if b in ("إذ", "وإذ", "فإذ") and n1 in IDH:
                out.append((key, ["idh_dhal", i, LETTER[n1]]))
            elif b in ("قد", "وقد", "فقد", "لقد", "ولقد") and n1 in QAD:
                out.append((key, ["qad_dal", i, LETTER[n1]]))
            elif b in ("هل", "بل", "فهل", "وهل") and n1 in HALBAL:
                out.append((key, ["hal_bal", i, LETTER[n1]]))
            elif b.endswith("ت") and final_sakin(key, i) and n1 in TA:
                out.append((key, ["ta_tanith", i, LETTER[n1]]))
            # حروف قربت مخارجها
            if b.endswith("يفعل") and final_sakin(key, i) and bare(nxt) == "ذلك":
                out.append((key, ["qarubat", i, "yf"]))
            if b.endswith("ب") and final_sakin(key, i) and n1 == "ف":
                out.append((key, ["qarubat", i, "bf"]))
            if key == "2:284" and b == "فيغفر":
                out.append((key, ["qarubat", i, "gh"]))
            if key == "2:284" and b == "ويعذب":
                out.append((key, ["qarubat", i, "yu"]))
        if nxc and b.endswith("ر") and final_sakin(key, i) and bare(nxc)[:1] == "ل":
            out.append((key, ["qarubat", i, "r" if nxt else "rv"]))
        if "لبثت" in b:
            out.append((key, ["qarubat", i, "lb"]))
        if "خذت" in b:
            L = letters(hafs_word(key, i))
            if any(L[j][0] == "ذ" and SUKUN in L[j][1] and L[j + 1][0] == "ت" for j in range(len(L) - 1)):
                out.append((key, ["qarubat", i, "akh"]))
        # النون الساكنة والتنوين قبل الواو والياء (من كلمتين)
        if nxc and bare(nxc)[:1] in "وي":
            L = last_letter(w)
            nun = L and L[-1][0] == "ن" and final_sakin(key, i)
            if nun or tanwin_at(key, i):
                f = "w" if bare(nxc)[:1] == "و" else "y"
                out.append((key, ["nun_sakina", i, f if nxt else f + "v"]))
    return out
