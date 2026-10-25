"""إمالة ذوات الياء وتقليلها (الشاطبية 291–317، 335–338). Rows: ["imala", i, flag?].
The flag is the place type (base) plus "w" when the alif is pronounced only in pause (a sakin or tanwin follows):
  ""  ordinary: Hamza & al-Kisa'i imala, Warsh taqlil with khulf          "w"  same, pause only
  "f" fa'la/fu'la/fi'la (alif al-ta'nith): + Abu Amr taqlil               "fw" same, pause only
  "r" alif after ra: Warsh taqlil (one way), Abu Amr imala               "rw" same, pause only (+ al-Susi's khulf in the ra in wasl)
  "a" annā: + al-Duri 'an Abi Amr taqlil
  "n" al-ribā: Hamza & al-Kisa'i only (Warsh opens it)
  "k" al-Kisa'i only, Warsh khulf      "kn" al-Kisa'i only, Warsh opens (marḍāt)      "dk" al-Duri 'an al-Kisa'i only, Warsh khulf"""
import re
from common import *

NOT_IMALA = {"على", "إلى", "حتى", "لدى"}
ALIF_WORDS = {"الدنيا": "", "والدنيا": "", "بالدنيا": "", "الربا": "n", "الربواا": "n", "والربواا": "n", "بسيماهم": "", "سيماهم": "",
              "خطاياكم": "k", "مرضات": "kn", "مرضاة": "kn", "فأحياكم": "k", "أحياكم": "k", "فأحيا": "k", "أحياهم": "k", "هداي": "dk"}
PRON = r"(ه|هم|هما|هن|ها|ك|كم|نا|ني)$"
# fa'la / fu'la / fi'la with alif al-ta'nith (al-Wafi p.150 lists the twenty fu'la, eleven fa'la, four fi'la words), for Abu Amr's taqlil
FU3LA = {"موسى", "عيسى", "يحيى", "دنيا", "قربى", "أنثى", "وسطى", "قصوى", "عزى", "وثقى", "حسنى", "أولى", "سفلى", "عليا", "رؤيا", "طوبى",
         "مثلى", "سوأى", "زلفى", "سقيا", "رجعى", "عقبى", "سلوى", "موتى", "تقوى", "نجوى", "قتلى", "مرضى", "دعوى", "شتى", "صرعى", "طغوى",
         "إحدى", "ضيزى", "سيما"}
ANNA = {"أنى", "فأنى"}

def kubra(w, nxt):
    b = bare(w)
    if b in ALIF_WORDS: return ALIF_WORDS[b]
    if re.search(r"ى" + PRON, b): return ""
    if not b.endswith("ى"): return None
    if b in NOT_IMALA or re.sub(r"^(و|ف)", "", b) in NOT_IMALA: return None
    L = letters(w)
    before = L[-2][1] if len(L) >= 2 else ""
    if FATHA not in before or (nxt is not None and starts_wasl(nxt)): return "w"
    return ""

def stem(b):
    """The word without an attached pronoun (on ى or ا) and without proclitics."""
    b = re.sub(r"(?<=[ىا])" + PRON, "", b)
    return b

def kind(w):
    """Base type for Warsh / Abu Amr: "r", "f", "a" or ""."""
    s = stem(bare(w))
    if len(s) >= 2 and s[-1] in "ىا" and s[-2] == "ر": return "r"
    if s in ANNA: return "a"
    core = re.sub(r"^(يا|و|ف|ب|ل)?(ال|ل)?", "", s)
    if core in FU3LA or s in FU3LA: return "f"
    return ""

def detect(vw):
    out = []
    for key, words, i, nxt, _ in words_iter(vw):
        r = kubra(words[i], nxt)
        if r is None: continue
        if r in ("", "w"):
            r = kind(words[i]) + r
        out.append((key, ["imala", i, r] if r else ["imala", i]))
    return out
