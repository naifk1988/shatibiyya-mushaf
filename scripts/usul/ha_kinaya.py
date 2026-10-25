"""باب هاء الكناية (الشاطبية 158–159): صلة هاء الضمير الواقعة بعد ساكن وقبل متحرك لابن كثير (فِيهِ هُدًى، مِنْهُ آيَاتٌ، اجْتَبَاهُ وَهَدَاهُ).
Rows: ["ha_kinaya", i]. Within the ayah only (the sila is a wasl feature). Fatiha/Baqarah have no word from 160–167."""
from common import *

ALLAH = {"الله", "لله", "بالله", "فالله", "والله", "تالله", "ولله", "فلله"}

def ha_after_sakin(w):
    b, L = bare(w), letters(w)
    if len(L) < 2 or L[-1][0] != "ه": return False
    m = L[-1][1]
    if not (DAMMA in m or KASRA in m) or has_tanwin(m) or SHADDA in m: return False
    if b in ALLAH or b.endswith("اله") or b.endswith("لاه"): return False     # الهاء الأصلية (إِلَاهُ)
    pa, pm = L[-2]
    if pa in "اى": return True                                  # اجْتَبَاهُ، ءَاتَىهُ
    if pa == "و" and len(L) >= 3 and DAMMA in L[-3][1] and not pm: return True     # عَقَلُوهُ (واو مد)
    if pa == "ي" and not pm: return True                         # فِيهِ، عَلَيْهِ (مد أو لين)
    if pa == "ي" and SUKUN in pm: return True
    return SUKUN in pm and SHADDA not in pm                     # مِنْهُ، فَلْيَصُمْهُ

def detect(vw):
    out = []
    for key, words, i, nxt, _ in words_iter(vw):
        if nxt and not starts_wasl(nxt) and ha_after_sakin(words[i]):
            out.append((key, ["ha_kinaya", i]))
    return out
