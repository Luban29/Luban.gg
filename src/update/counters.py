"""Turn raw Lolalytics counters into the counter files in src/e30/.

Input: a JSON file from src/collect/lolalytics.js (LUBAN.out.raw): {"lane|Name": {slug, wr, pr, lanes, def, rows}},
rows = [[opponent, enemy's win rate against it, games, opponent's main lane]] with 100+ games, Emerald+, last 30 days.

Output (same formats as before, see sel.py and ten.py):
  e30/pools.txt   champions really played in each lane (pick rate >= 1 %, or >= 0.5 % when the lane is at least a quarter
                  of their games) with pick rate and lane win rate; after "#" the six best picks against each class
  e30/pr.txt      pick rates of enemies with no usable matchup in a lane (used for the "skoro se nehraje" note)
  e30/<lane>.tsv  enemy, mode, games, chosen picks (main + up to three alternatives)
  e30/more.tsv    further direct picks up to ten in total
  e30/cls10.tsv   up to 14 picks with the best win rate against each class

Picks are ranked by win rate minus 100/sqrt(games). Modes: E = a pick with 300+ games wins more than half,
S = only picks with fewer than 300 games win more than half, L = picks with 300+ games exist but none wins,
N = no usable pick (sel.py turns S without a winner into N too, then uses class picks or kit-based picks).

Usage: python3 src/update/counters.py raw.json
"""
import json, math, os, sys
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
sys.path.insert(0, SRC)
from meta import M
from dump_missing import canon, key

LANES = ["top", "jungle", "mid", "bottom", "support"]
LQ = {"top": "top", "jungle": "jungle", "mid": "middle", "bottom": "bottom", "support": "support"}
LANE_CODE = {"top": "t", "jungle": "j", "mid": "m", "bottom": "b", "support": "s"}
CLASS_CODE = {"tank": "t", "bruiser": "b", "assassin": "a", "mage": "m", "adc": "c", "enchanter": "e", "catcher": "k", "specialist": "s"}
B36 = "0123456789abcdefghijklmnopqrstuvwxyz"
ORDER = sorted(M, key=key)
CODE = {n: (B36[i] if i < 36 else B36[i // 36] + B36[i % 36]) for i, n in enumerate(ORDER)}


def fixed(x, d):
    """JavaScript toFixed(d): the exact binary value rounded, ties up (the old files were written that way)."""
    return format(Decimal(x).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP), "f")


def jsnum(x):
    return str(int(x)) if float(x) == int(x) else repr(float(x))


def score(wr, n):
    return wr - 100 / math.sqrt(n)


def load(path):
    raw, skipped = {}, set()
    for k, d in json.load(open(path, encoding="utf-8")).items():
        lane, name = k.split("|", 1)
        try:
            name = canon(name)
        except KeyError:
            skipped.add(name)
            continue
        rows = []
        for r in d["rows"]:
            try:
                rows.append([canon(r[0])] + list(r[1:]))
            except KeyError:
                skipped.add(r[0])
        raw[(lane, name)] = dict(d, rows=rows)
    if skipped:
        print("not in meta.py (new champion? add class and tip there):", sorted(skipped))
    return raw


def build(raw):
    names = sorted({n for _, n in raw}, key=key)
    pools = {}
    for lane in LANES:
        pools[lane] = [n for n in names if (lane, n) in raw and
                       (raw[(lane, n)]["pr"] >= 1 or (raw[(lane, n)]["pr"] >= 0.5 and raw[(lane, n)]["lanes"].get(LQ[lane], 0) >= 25))]

    def cands(lane, e):
        out = []
        for name, vs, n, _ in raw[(lane, e)]["rows"]:
            if name == e or name not in pools[lane] or n < 100:
                continue
            wr = 100 - vs
            out.append((name, wr, n, score(wr, n)))
        out.sort(key=lambda r: -r[3])
        return out

    sel, eff = {}, {}
    for lane in LANES:
        for e in names:
            if (lane, e) not in raw:
                continue
            tot = sum(r[2] for r in raw[(lane, e)]["rows"])
            C = cands(lane, e)
            wins = [c for c in C if c[1] > 50]
            bigw = [c for c in wins if c[2] >= 300]
            if not C:
                mode, picks = "N", []
            elif bigw:
                mode, picks = "E", [bigw[0]] + [c for c in wins if c is not bigw[0]][:3]
            elif wins:
                mode, picks = "S", wins[:4]
            elif any(c[2] >= 300 for c in C):
                mode, picks = "L", [next(c for c in C if c[2] >= 300)]
            else:
                mode, picks = "S", C[:1]
            sel[(lane, e)] = (mode, tot, picks, C)
            eff[(lane, e)] = "N" if mode == "N" or (mode == "S" and picks[0][1] <= 50) else mode

    def agg(lane, cls):
        G = {}
        for e in names:
            if (lane, e) not in raw or M[e][0] != cls:
                continue
            for name, vs, n, _ in raw[(lane, e)]["rows"]:
                if name == e or name not in pools[lane] or n < 100:
                    continue
                g = G.setdefault(name, [0, 0.0])
                g[0] += n
                g[1] += n * (100 - vs) / 100
        rows = [(nm, 100 * w / n, n) for nm, (n, w) in G.items()]
        rows.sort(key=lambda r: -score(r[1], r[2]))
        return rows

    files = {}
    lines = []
    for lane in LANES:
        lines.append(lane + "\t" + ",".join(f"{n}:{jsnum(raw[(lane, n)]['pr'])}:{jsnum(raw[(lane, n)]['wr'])}" for n in pools[lane]))
    lines.append("#")
    classes = sorted({M[n][0] for n in M})
    for lane in sorted(LANES):
        for cls in classes:
            rows = [r for r in agg(lane, cls) if r[2] >= 1000][:6]
            lines.append(f"{lane}|{cls}\t" + ",".join(f"{n}:{fixed(w, 2)}:{g}" for n, w, g in rows))
    files["pools.txt"] = "\n".join(lines) + "\n"
    files["pr.txt"] = "".join(
        lane + "\t" + ",".join(f"{key(e)}={jsnum(raw[(lane, e)]['pr'])}" for e in names if eff.get((lane, e)) == "N") + "\n"
        for lane in LANES)
    for lane in LANES:
        files[lane + ".tsv"] = "".join(
            f"{e}\t{sel[(lane, e)][0]}\t{sel[(lane, e)][1]}\t" + ",".join(f"{n}:{fixed(w, 1)}:{g}" for n, w, g, _ in sel[(lane, e)][2]) + "\n"
            for e in names if (lane, e) in sel)
    more = []
    for lane in LANES:
        for e in names:
            if (lane, e) not in sel or eff[(lane, e)] == "N":
                continue
            mode, tot, picks, C = sel[(lane, e)]
            have = {p[0] for p in picks}
            rest = [c for c in C if c[0] not in have]
            rest = [c for c in rest if c[1] > 50] + [c for c in rest if c[1] <= 50]
            rest = rest[:max(0, 10 - len(picks))]
            if rest:
                more.append(LANE_CODE[lane] + CODE[e] + "\t" + ",".join(f"{CODE[n]}:{fixed(w, 1)}:{g}" for n, w, g, _ in rest))
    files["more.tsv"] = "\n".join(more) + "\n"
    cls10 = []
    for lane in LANES:
        for cls, c in CLASS_CODE.items():
            full = agg(lane, cls)
            full = ([r for r in full if r[1] > 50] + [r for r in full if r[1] <= 50])[:14]
            if full:
                cls10.append(LANE_CODE[lane] + c + "\t" + ",".join(f"{CODE[n]}:{fixed(w, 1)}:{g}" for n, w, g in full))
    files["cls10.tsv"] = "\n".join(cls10) + "\n"
    return files, pools, eff


if __name__ == "__main__":
    raw = load(sys.argv[1])
    files, pools, eff = build(raw)
    out = os.path.join(SRC, "e30")
    for name, text in files.items():
        open(os.path.join(out, name), "w", encoding="utf-8").write(text)
    from collections import Counter
    print("pools:", {l: len(v) for l, v in pools.items()})
    print("modes:", dict(Counter(eff.values())))
    print("written:", ", ".join(sorted(files)))
