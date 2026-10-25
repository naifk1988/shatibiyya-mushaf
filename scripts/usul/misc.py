"""Small usul chapters (al-Fatiha + al-Baqarah):
- zawaid (ياءات الزوائد 420–436): الداعِ/دعانِ 2:186 (flags d/n), واتقونِ يا أولي 2:197 (flag t).
- basmala (البسملة 100–107): first word of 2:1, between al-Fatiha and al-Baqarah.
- istiadha (الاستعاذة 95–99): first word of 1:1 (no reader differs; card only).
- waqf_ta (مرسوم الخط 378–379): هاء التأنيث written with ت — رحمت/نعمت (flags r/n), مرضات (flag m, al-Kisa'i only).
- waqf_sakt (مرسوم الخط 386): لِمَ/بِمَ/فِيمَ/عَمَّ/مِمَّ — al-Bazzi's ha' al-sakt (bi-khulf).
Rows: [rule, i] or [rule, i, flag]."""
import re
from common import *

# zawa'id of al-Baqarah per al-Wafi (the only ones of the seven in these two surahs); matched on the bare q4 word + its neighbour
ZAWAID = [
    ("الداع", "اذا", "d"),        # أجيب دعوة الداعِ إذا دعانِ
    ("دعان", "فليستجيبوا", "n"),
    ("واتقون", "ياأولي", "t"),     # واتقونِ يا أولي الألباب (q4 joins يا+أولي)
]
TA_WORDS = {"رحمت": "r", "نعمت": "n"}           # ha' al-ta'nith written ت (other such nouns do not occur in 1–2)
TA_OTHER = ("امرأت", "سنت", "لعنت", "معصيت", "كلمت", "بقيت", "قرت", "فطرت", "شجرت", "جنت", "ابنت")
SAKT = ("لم", "بم", "فيم", "عم", "مم")

def strip_wa_fa(b):
    return b[1:] if len(b) > 2 and b[0] in "وف" else b

def detect(vw):
    out = []
    out.append(("1:1", ["istiadha", 0]))
    out.append(("2:1", ["basmala", 0]))
    for key, words, i, nxt, _ in words_iter(vw):
        w = words[i]; b = bare(w).replace("ٱ", "ا"); nb = bare(nxt).replace("ٱ", "ا").replace("أ", "ا").replace("إ", "ا") if nxt else ""
        # zawa'id: final letter written without ya, wasl only (so the next word must exist in the same ayah)
        for word, after, flag in ZAWAID:
            if b == word and nb.replace("ْ", "").startswith(after.replace("أ", "ا")) and last_letter(w)[-1][0] != "ي":
                out.append((key, ["zawaid", i, flag]))
        # ha' al-ta'nith written with ت
        core = strip_wa_fa(b)
        if core in TA_WORDS:
            out.append((key, ["waqf_ta", i, TA_WORDS[core]]))
        elif core in TA_OTHER:
            out.append((key, ["waqf_ta", i]))
        elif core == "مرضات":
            out.append((key, ["waqf_ta", i, "m"]))
        # interrogative ما after a preposition, alif dropped: لِمَ بِمَ فِيمَ عَمَّ مِمَّ (not لَمْ)
        if strip_wa_fa(b) in SAKT:
            L = letters(w)
            if L and L[-1][0] == "م" and FATHA in L[-1][1] and SUKUN not in L[-1][1]:
                out.append((key, ["waqf_sakt", i]))
    return out
