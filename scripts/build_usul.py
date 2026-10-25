#!/usr/bin/env python3
"""Build the usul layer from the detectors in scripts/usul/*.py and the rule cards in data/usul/*.json.
Each detector module has detect(vw) -> [(ayahKey, [ruleId, wordIndex, flag?]), ...]; rule ids must have a card in data/usul/<id>.json.
Output: data/u/<surah>.json {"s:a": [[rule, i, flag?], ...]} and data/usul_rules.json {id: card}.
Run: python3 scripts/build_usul.py [--list [ruleId]]"""
import json, glob, os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "usul"))
from common import ROOT, load_vw, SURAHS

def main():
    vw = load_vw()
    cards = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "usul", "*.json"))):
        c = json.load(open(f, encoding="utf-8")); cards[c["id"]] = c
    out = {s: {} for s in SURAHS}; tot = {}; problems = []
    for f in sorted(glob.glob(os.path.join(HERE, "usul", "*.py"))):
        name = os.path.basename(f)[:-3]
        if name == "common": continue
        mod = importlib.import_module(name)
        if not hasattr(mod, "detect"): continue
        for key, row in mod.detect(vw):
            if row[0] not in cards: problems.append(f"{name}: no card for rule {row[0]}"); continue
            s = int(key.split(":")[0])
            lst = out[s].setdefault(key, [])
            if row not in lst: lst.append(row); tot[row[0]] = tot.get(row[0], 0) + 1
    for d in out.values():
        for k in d: d[k].sort(key=lambda r: (r[1], r[0]))
    os.makedirs(os.path.join(ROOT, "data", "u"), exist_ok=True)
    for s, d in out.items():
        json.dump(d, open(os.path.join(ROOT, "data", "u", f"{s}.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump(cards, open(os.path.join(ROOT, "data", "usul_rules.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("places:", dict(sorted(tot.items())))
    for p in sorted(set(problems)): print("!", p)
    if "--list" in sys.argv:
        only = sys.argv[sys.argv.index("--list") + 1] if len(sys.argv) > sys.argv.index("--list") + 1 else None
        for s, d in out.items():
            for key, rows in d.items():
                ws = vw[key]
                for r in rows:
                    if only and r[0] != only: continue
                    nx = ws[r[1] + 1] if r[1] + 1 < len(ws) else "⟂"
                    print(key, r[0], (r[2] if len(r) > 2 else ""), ws[r[1]], "→", nx)

if __name__ == "__main__":
    main()
