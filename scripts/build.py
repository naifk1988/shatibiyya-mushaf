#!/usr/bin/env python3
"""Merge data/raw/*.json (one file per extraction range) into the files the app reads:
   data/shatibiyya.json  — index: sources, coverage, counts
   data/s/<surah>.json   — {"surah:ayah": [entry, ...]} loaded when a page of that surah opens
Run from the project root:  python3 scripts/build.py
"""
import json, glob, os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
OUT_S = os.path.join(ROOT, "data", "s")
FIELDS = ["bayt_no", "bayt_to", "bayt", "cue", "also", "all", "readings", "ramz", "ma3na", "tawjih", "wafi_loc", "kashf_loc", "note"]

def load_raw():
    rows = []
    for f in sorted(glob.glob(os.path.join(RAW, "*.json"))):
        if os.path.basename(f) == "matn_vocalized.json": continue
        try:
            data = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            sys.exit(f"bad JSON in {f}: {e}")
        for r in data:
            r["_src"] = os.path.basename(f)
            rows.append(r)
    return rows

def main():
    rows = load_raw()
    # the vocalized matn (corrected from «متن الشاطبية», Khizana 7754) replaces al-Wafi's unvocalized bayt text
    vf = os.path.join(RAW, "matn_vocalized.json")
    voc = json.load(open(vf, encoding="utf-8")) if os.path.exists(vf) else {}
    for r in rows:
        nos = range(r["bayt_no"], (r.get("bayt_to") or r["bayt_no"]) + 1)
        if voc and all(str(n) in voc for n in nos):
            r["bayt"] = "\n".join(voc[str(n)] for n in nos)
    by_surah = defaultdict(lambda: defaultdict(list))
    bayts, problems = set(), []
    for r in rows:
        bayts.update(range(r.get("bayt_no") or 0, (r.get("bayt_to") or r.get("bayt_no") or 0) + 1))
        if not r.get("bayt"): problems.append(f"{r['_src']} bayt {r.get('bayt_no')}: no bayt text")
        for k in r.get("keys") or []:
            if not re.fullmatch(r"\d+:\d+", k): problems.append(f"{r['_src']} bad key {k}"); continue
            s = k.split(":")[0]
            e = {f: r[f] for f in FIELDS if r.get(f) not in (None, "", [])}
            # the same bayt can name the same word twice (e.g. two rules); keep one card per bayt+cue
            if not any(x["bayt_no"] == e["bayt_no"] and x["cue"] == e["cue"] for x in by_surah[s][k]):
                by_surah[s][k].append(e)
    os.makedirs(OUT_S, exist_ok=True)
    for f in glob.glob(os.path.join(OUT_S, "*.json")): os.remove(f)
    total = 0
    for s, entries in by_surah.items():
        for k in entries: entries[k].sort(key=lambda e: e["bayt_no"])
        total += sum(len(v) for v in entries.values())
        json.dump(entries, open(os.path.join(OUT_S, f"{s}.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    covered = sorted(int(s) for s in by_surah)
    index = {
        "version": 1, "split": True, "total": total, "bayts": len(bayts),
        "surahs_covered": covered,
        "coverage": "سورة الفاتحة وسورة البقرة" if covered == [1, 2] else f"{len(covered)} سورة",
        "sources": [
            {"id": "matn", "title": "حرز الأماني ووجه التهاني (الشاطبية)", "author": "القاسم بن فيره الشاطبي", "death": 590},
            {"id": "wafi", "title": "الوافي في شرح الشاطبية", "author": "عبد الفتاح القاضي", "death": 1403, "khizana": 38075},
            {"id": "kashf", "title": "الكشف عن وجوه القراءات السبع وعللها وحججها", "author": "مكي بن أبي طالب القيسي", "death": 437, "khizana": 1271},
        ],
    }
    json.dump(index, open(os.path.join(ROOT, "data", "shatibiyya.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(rows)} records, {len(bayts)} bayts, {total} ayah-cards, surahs {covered}")
    for p in problems: print("!", p)

if __name__ == "__main__":
    main()
