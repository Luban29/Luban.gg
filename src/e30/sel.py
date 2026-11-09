# Selection from fresh Emerald+ data (last 30 days, fetched 7 Nov 2026).
# e30/<lane>.tsv: enemy, mode, enemy games in lane, picks as Name:pickWR:games (main first, ranked by WR - 100/sqrt(games)).
#   E = main pick has 300+ games and WR > 50, L = 300+ games but nobody above 50 %, S = only small samples (30-299 games),
#   N = no lane pick has even 30 games against this enemy.
# Only champions commonly played in the lane are considered: Emerald+ pick rate >= 1 %, or >= 0.5 % when the lane
# makes up at least a quarter of that champion's games (pools.txt).
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from meta import M
from exc import EXC
from dump_missing import canon

LANES = ["top", "jungle", "mid", "bottom", "support"]
D = HERE + os.sep

def load_pools():
    pools, cls = {}, {}
    part = 0
    for line in open(D + "pools.txt", encoding="utf-8"):
        line = line.rstrip("\n")
        if line == "#":
            part = 1
            continue
        k, v = line.split("\t")
        rows = []
        for x in filter(None, v.split(",")):
            n, a, b = x.rsplit(":", 2)
            rows.append((canon(n), float(a), float(b)))
        if part == 0:
            pools[k] = {n: (pr, wr) for n, pr, wr in rows}     # name -> (pick rate %, lane win rate %)
        else:
            lane, c = k.split("|")
            cls[(lane, c)] = [(n, wr, int(g)) for n, wr, g in rows]  # pick, WR vs that class, games
    return pools, cls

POOLS, CLS = load_pools()

def class_picks(lane, enemy):
    c = M[enemy][0]
    rows = [r for r in CLS.get((lane, c), []) if r[1] > 50 and r[0] != enemy]
    solid = [r for r in rows if r[1] - 100 / r[2] ** 0.5 > 49]
    return rows[:3] if len(solid) >= 2 else None

def entries():
    """Yield (lane, enemy, mode, tot, picks); picks are (name, wr, games). For X picks games = 0 and wr is the lane WR."""
    for lane in LANES:
        for line in open(D + lane + ".tsv", encoding="utf-8"):
            e, mode, tot, picks = line.rstrip("\n").split("\t")
            e, tot = canon(e), int(tot)
            rows = []
            for p in filter(None, picks.split(",")):
                n, wr, g = p.rsplit(":", 2)
                rows.append((canon(n), float(wr), int(g)))
            if mode == "S" and rows and rows[0][1] <= 50:
                mode = "N"
            if mode == "N":
                cp = class_picks(lane, e)
                if cp:
                    mode, rows = "C", cp
                else:
                    mode = "X"
                    rows = []
                    for p, _ in EXC[(lane, M[e][0])]:
                        if p not in POOLS[lane]:
                            raise SystemExit(f"EXC pick {p} not played in {lane}")
                        rows.append((p, POOLS[lane][p][1], 0))
            yield lane, e, mode, tot, rows

if __name__ == "__main__":
    from dump_missing import load_have
    have = load_have()
    want = sys.argv[1] if len(sys.argv) > 1 else None
    cnt, miss, clsneed = {}, {}, {}
    for lane, e, mode, tot, rows in entries():
        cnt.setdefault(lane, {}).setdefault(mode, 0)
        cnt[lane][mode] += 1
        if mode in "ELS":
            for i, (p, wr, g) in enumerate(rows):
                if (lane, e, p) not in have:
                    miss.setdefault(lane, []).append((e, p, i == 0))
        elif mode == "C":
            clsneed.setdefault((lane, M[e][0]), [r[0] for r in rows])
    for lane in LANES:
        print(lane, cnt[lane], "missing reasons:", len(miss.get(lane, [])))
    print("class combos:", len(clsneed))
    if want == "cls":
        for k, v in sorted(clsneed.items()):
            print(k, v)
    elif want:
        cur = None
        for e, p, main in miss.get(want, []):
            print(f"{e}|{p}{'*' if main else ''}")
