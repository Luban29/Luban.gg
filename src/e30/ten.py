# Up to ten counter picks per enemy and lane (Emerald+, last 30 days, data fetched 10 Nov 2026).
# Order: the picks chosen before (main + alternatives with written reasons), then more direct matchups
# (winners first, then the rest by reliability), then picks by the enemy's class, then the lane's strongest champions.
# Pick = [name, wr, games, why or None, kind, vs]; kind 0 main, 1 alt, 2 by class, 3 strong in lane;
# vs 0 = matchup win rate, 1 = win rate vs the enemy's class, 2 = overall lane win rate.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
from meta import M
from dump_missing import key
from sel import entries, POOLS, class_picks

D = HERE + os.sep
ORDER = sorted(M, key=key)
B36 = "0123456789abcdefghijklmnopqrstuvwxyz"
CODE = {}
for i, n in enumerate(ORDER):
    CODE[B36[i] if i < 36 else B36[i // 36] + B36[i % 36]] = n
LANE = {"t": "top", "j": "jungle", "m": "mid", "b": "bottom", "s": "support"}
CLS = {"t": "tank", "b": "bruiser", "a": "assassin", "m": "mage", "c": "adc", "e": "enchanter", "k": "catcher", "s": "specialist"}

def picks(s):
    out = []
    for x in filter(None, s.split(",")):
        c, wr, g = x.split(":")
        out.append((CODE[c], float(wr), int(g)))
    return out

MORE = {}
for line in open(D + "more.tsv", encoding="utf-8"):
    k, v = line.rstrip("\n").split("\t")
    MORE[(LANE[k[0]], CODE[k[1:]])] = picks(v)
CLS10 = {}
for line in open(D + "cls10.tsv", encoding="utf-8"):
    k, v = line.rstrip("\n").split("\t")
    CLS10[(LANE[k[0]], CLS[k[1]])] = picks(v)
STRONG = {lane: sorted(POOLS[lane], key=lambda n: -POOLS[lane][n][1]) for lane in POOLS}

def split50(ps):
    """Inside each block of picks measured the same way, picks over 50 % come before the rest (order kept otherwise).
    The first pick stays first: it is the chosen main counter, and when it is not over 50 % no pick in its block is."""
    out, i = ps[:1], 1
    while i < len(ps):
        j = i
        while j < len(ps) and (ps[j][4] == 3) == (ps[i][4] == 3) and ps[j][5] == ps[i][5] and (ps[j][4] == 2) == (ps[i][4] == 2):
            j += 1
        block = ps[i:j]
        out += [p for p in block if p[1] > 50] + [p for p in block if p[1] <= 50]
        i = j
    return out

def build(why_direct, why_class, why_kit):
    """Return {lane: {enemy: [mode, pr_or_None, picks]}}; why_* are callables giving a written reason or None."""
    out = {}
    for lane, e, mode, tot, rows in entries():
        cls = M[e][0]
        ps, have = [], set()
        def add(n, wr, g, why, kind, vs):
            if n in have or n == e or len(ps) >= 10:
                return
            have.add(n)
            ps.append([n, round(wr, 1), g, why, kind, vs])
        if mode in "ELS":
            for i, (n, wr, g) in enumerate(rows):
                add(n, wr, g, why_direct(lane, e, n), 0 if i == 0 else 1, 0)
            for n, wr, g in MORE.get((lane, e), []):
                add(n, wr, g, None, 1, 0)
            # thin small-sample cards were filled with class picks before; keep those first among the class picks
            prev = class_picks(lane, e) if mode == "S" and len(rows) < 3 else None
            for n, wr, g in (prev or []) + CLS10.get((lane, cls), []):
                add(n, wr, g, why_class(lane, cls, n), 2, 1)
        elif mode == "C":
            for i, (n, wr, g) in enumerate(rows):
                add(n, wr, g, why_class(lane, cls, n), 0 if i == 0 else 1, 1)
            for n, wr, g in CLS10.get((lane, cls), []):
                add(n, wr, g, why_class(lane, cls, n), 1, 1)
        else:  # X: kit-based picks with their overall lane win rate
            for i, (n, wr, g) in enumerate(rows):
                add(n, wr, 0, why_kit(lane, cls, n), 0 if i == 0 else 1, 2)
        for n in STRONG[lane]:
            add(n, POOLS[lane][n][1], 0, None, 3, 2)
        out.setdefault(lane, {})[e] = [mode, split50(ps)]
    return out

if __name__ == "__main__":
    from dump_missing import load_have
    from cls_why import CLS_WHY
    from exc import EXC
    have = load_have()
    EXCW = {(l, c, p): t for (l, c), v in EXC.items() for p, t in v}
    res = build(lambda l, e, n: have.get((l, e, n)), lambda l, c, n: CLS_WHY.get((l, c, n)), lambda l, c, n: EXCW.get((l, c, n)))
    from collections import Counter
    sizes = Counter(len(v[1]) for d in res.values() for v in d.values())
    kinds = Counter(p[4] for d in res.values() for v in d.values() for p in v[1])
    nowhy = sorted({(l, p[0]) for l, d in res.items() for v in d.values() for p in v[1] if not p[3]})
    print("list sizes", dict(sizes), "kinds", dict(kinds))
    print("lane+pick pairs needing a generic line:", len(nowhy))
    for lane in ["top", "jungle", "mid", "bottom", "support"]:
        print(lane, [p for l, p in nowhy if l == lane])
