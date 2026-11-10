"""Write the Items tab data in src/items/ from what the collectors gathered.

Inputs: builds.json from src/collect/lolalytics.js ({"lol": {"Name|lane": line}, "full": {...}, "items": {id: name}})
and pro.json from src/collect/proslol.js ({"Name|lane": line}).
Outputs: items/lol.tsv, items/full.tsv, items/pro.tsv and new item names appended to items/items.tsv.

Usage: python3 src/update/items.py builds.json pro.json
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
sys.path.insert(0, SRC)
from dump_missing import canon, key

LANES = ["top", "jungle", "mid", "bottom", "support"]
D = os.path.join(SRC, "items")


def rows(d):
    out = []
    for k, v in d.items():
        name, lane = k.rsplit("|", 1)
        out.append((key(canon(name)), LANES.index(lane), canon(name), lane, v))
    return [r[2:] for r in sorted(out)]


def main(builds_path, pro_path):
    b = json.load(open(builds_path, encoding="utf-8"))
    pro = json.load(open(pro_path, encoding="utf-8"))
    lol = rows(b["lol"])
    full = rows(b["full"])
    pros = rows(pro)
    if {(n, l) for n, l, _ in lol} != {(n, l) for n, l, _ in full}:
        raise SystemExit("builds and full builds cover different champions")
    open(os.path.join(D, "lol.tsv"), "w", encoding="utf-8").write("".join(f"{n}\t{l}\t{v}\n" for n, l, v in lol))
    open(os.path.join(D, "full.tsv"), "w", encoding="utf-8").write("".join(f"{n}\t{l}\t{v}\n" for n, l, v in full))
    # pro line: games, games used, items, three games (the collector adds two timestamps, not used by the page)
    open(os.path.join(D, "pro.tsv"), "w", encoding="utf-8").write(
        "".join(f"{n}\t{l}\t" + "\t".join((v.split("\t") + ["", "", "", ""])[:4]) + "\n" for n, l, v in pros))
    # item names: keep the existing ones (Data Dragon names), add new ids with the Lolalytics name
    known = {}
    lines = open(os.path.join(D, "items.tsv"), encoding="utf-8").read().splitlines()
    for line in lines:
        i, name, _ = line.split("\t")
        known[int(i)] = name
    used = set()
    ids = lambda s: [int(x) for x in s.split("_") if x]
    for _, _, v in lol:
        f = v.split("\t")
        for part in (f[3], f[4], f[5], f[6]):
            for x in filter(None, part.split(";")):
                used.update(ids(x.split(":")[0]))
    for _, _, v in full:
        f = v.split("\t")
        for x in filter(None, f[0].split(";")):
            used.update(ids(x.split(":")[0]))
        used.update(int(x) for x in f[1].split(";") if x)
    for _, _, v in pros:
        f = (v.split("\t") + ["", "", "", ""])[:4]
        used.update(int(x.split(":")[0]) for x in f[2].split(";") if x)
        for g in filter(None, f[3].split("|")):
            used.update(ids(g.split(",")[-1]))
    names = {int(k): v for k, v in b["items"].items()}
    new = sorted(i for i in used if i not in known and i in names)
    bad = [i for i in new if not names[i] or "deprecated" in names[i].lower()]
    if bad:
        print("items without a usable name, look them up in Data Dragon:", bad)
    with open(os.path.join(D, "items.tsv"), "a", encoding="utf-8") as f:
        for i in new:
            if i not in bad:
                f.write(f"{i}\t{names[i]}\tx\n")
    print("builds:", len(lol), "pro lines:", len(pros), "with pro games:", sum(1 for *_, v in pros if not v.startswith("0\t")),
          "new item names:", [(i, names[i]) for i in new])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
