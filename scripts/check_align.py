#!/usr/bin/env python3
"""Check that every card's cue lands on a word of its ayah in the Madinah page data (same matching as index.html).
Prints the cards whose word could not be found, so the cue can be corrected in data/raw before publishing."""
import json, glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIAC = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ࣓-ࣿ]")

def norm(s):
    s = DIAC.sub("", str(s or ""))
    for a, b in (("ٱ", "ا"), ("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ى", "ي"), ("ة", "ه"), ("ؤ", "و"), ("ئ", "ي")):
        s = s.replace(a, b)
    s = re.sub(r"[^ء-ي ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"(^| )يا (?=\S)", r"\1يا", s)
    return s.replace("اليل", "الليل").replace("ص", "س")

def skel(s):
    n = norm(s)
    return re.sub(r"[اويءى ]", "", n) or n.replace(" ", "")

ORD = {"الأولى": 1, "الأول": 1, "الثاني": 2, "الثانية": 2, "الثالث": 3, "الثالثة": 3, "الرابع": 4, "الرابعة": 4}

def align(cue, words):
    nth = [1]
    def strip(m):
        x = m.group(1).strip()
        if x in ORD: nth[0] = ORD[x]
        return " "
    cue = re.sub(r"[(（\[]([^)\]）]*)[)\]）]", strip, str(cue or ""))
    toks = [t for t in norm(cue).split(" ") if t]
    if not toks: return -1
    def seq(f):
        t, W = [f(x) for x in toks], [f(x) for x in words]
        seen, last = 0, -1
        for i in range(len(W) - len(t) + 1):
            if W[i:i + len(t)] == t:
                seen += 1; last = i + len(t) - 1
                if seen == nth[0]: return last
        return last
    for f in (lambda x: norm(x).replace(" ", ""), skel):
        w = seq(f)
        if w >= 0: return w
    S, ends = "", []
    for k in map(skel, words):
        S += k; ends.append(len(S))
    def find(c):
        if not c: return -1
        i, seen, last = S.find(c), 0, -1
        while i != -1:
            if i + len(c) in ends:
                w = ends.index(i + len(c)); seen += 1; last = w
                if seen == nth[0]: return w
            i = S.find(c, i + 1)
        return last
    w = find("".join(map(skel, toks)))
    if w < 0 and len(toks) > 1: w = find(skel(toks[-1]))
    return w

def main():
    vw = {}
    for f in glob.glob(os.path.join(ROOT, "data", "q4", "*.json")):
        vw.update(json.load(open(f, encoding="utf-8"))["vw"])
    bad = n = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "s", "*.json"))):
        for key, cards in json.load(open(f, encoding="utf-8")).items():
            for c in cards:
                n += 1
                words = vw.get(key)
                if not words:
                    bad += 1; print(f"no ayah {key}"); continue
                w = align(c["cue"], words)
                if os.environ.get("SHOW"): print(key, c["bayt_no"], c["cue"], "→", words[w] if w >= 0 else "✗")
                if w < 0:
                    bad += 1; print(f"✗ {key} bayt {c['bayt_no']}: «{c['cue']}» not in: {' '.join(words)}")
    print(f"{n - bad}/{n} cards aligned")

if __name__ == "__main__":
    main()
