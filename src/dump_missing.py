import sys, re, json, glob, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from meta import M
from why import WHY
from alt_why import ALT_WHY
def key(s): return re.sub(r"[^a-z]", "", s.lower())
NAMES = {key(n): n for n in M}
NAMES.update({"nunu": "Nunu & Willump", "renata": "Renata Glasc", "monkeyking": "Wukong"})
canon = lambda s: NAMES[key(s)]
def load_have():
    have = {}
    for l, d in WHY.items():
        for e, (p, t) in d.items(): have[(l, canon(e), canon(p))] = t
    for l, d in ALT_WHY.items():
        for e, m in d.items():
            for p, t in m.items(): have[(l, canon(e), canon(p))] = t
    for f in glob.glob(os.path.join(HERE, "reasons", "*.txt")):
        lane = os.path.basename(f).split(".")[0].split("_")[0]
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"): continue
            e, p, t = line.split("|", 2)
            have[(lane, canon(e), canon(p))] = t
    return have
def selection():
    out = []
    for line in open(os.path.join(HERE, "raw30.tsv"), encoding="utf-8"):
        l, e, tier, wrE, picks = line.rstrip("\n").split("\t")
        if not picks: continue
        rows = []
        for p in picks.split(","):
            n, wr, g = p.rsplit(":", 2)
            rows.append((canon(n), 100 - float(wr), int(g)))
        rows.sort(key=lambda r: -(r[1] - 100 / r[2] ** 0.5))
        reg = [r for r in rows if r[2] >= 300 and r[1] > 50]
        main = reg[0] if reg else rows[0]
        alts = [r for r in rows if r is not main and r[1] > 50][:3]
        out.append((l, canon(e), main, alts))
    return out
if __name__ == "__main__":
    lane = sys.argv[1]
    have = load_have()
    n = 0
    for l, e, main, alts in selection():
        if l != lane: continue
        miss = [r[0] + ("*" if r is main else "") for r in [main] + alts if (l, e, r[0]) not in have]
        if miss:
            n += len(miss)
            print(f"{e}: {', '.join(miss)}")
    print("total", n, file=sys.stderr)
