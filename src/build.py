import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "e30"))
from meta import M
from exc import EXC
from dump_missing import key, load_have, canon
from sel import LANES
from cls_why import CLS_WHY

# Emerald+ only, last 30 days (fetched 10 Nov 2026). Modes from e30/sel.py:
#   E = reliable winner (300+ games), L = reliable picks but none above 50 %, S = winners only with small samples,
#   C = enemy barely played in the lane, picks by win rate against the enemy's class,
#   X = not even class data, picks by kit with their overall lane win rate.
# Entry: [mode, enemy pick rate in the lane % (C/X, else 0), ten picks]; pick = [name, wr, games, why, kind, vs]
#   why = written reason, or 0 = use the pick's lane line from G (what it does well in that lane)
#   kind 0 main, 1 alt, 2 by class, 3 strong in lane; vs 0 matchup, 1 vs the enemy's class, 2 overall lane win rate
from ten import build as build_ten
from lane_why import LANE_WHY
REASON = load_have()
EXCW = {(l, c, p): t for (l, c), v in EXC.items() for p, t in v}
nk = lambda s: re.sub(r"[^a-z]", "", s.lower())
PR = {}
for line in open(os.path.join(HERE, "e30", "pr.txt"), encoding="utf-8"):
    lane, v = line.rstrip("\n").split("\t")
    for x in v.split(","):
        n, p = x.split("=")
        PR[(lane, n)] = float(p)

ten = build_ten(lambda l, e, n: REASON.get((l, e, n)), lambda l, c, n: CLS_WHY.get((l, c, n)), lambda l, c, n: EXCW.get((l, c, n)))
out, counts, G = {}, {}, {}
for lane, d in ten.items():
    for e, (mode, ps) in d.items():
        if len(ps) != 10 or any(p[0] == e for p in ps) or len({p[0] for p in ps}) != 10:
            raise SystemExit(f"bad list {lane} {e}")
        if mode in "ELS" and not ps[0][3]:
            raise SystemExit(f"main pick without reason {lane} {e}")
        for p in ps:
            if not p[3]:
                if (lane, p[0]) not in LANE_WHY:
                    raise SystemExit(f"no lane line {lane} {p[0]}")
                G.setdefault(lane, {})[p[0]] = LANE_WHY[(lane, p[0])]
                p[3] = 0
        out.setdefault(lane, {})[e] = [mode, PR[(lane, nk(e))] if mode in "CX" else 0, ps]
        counts.setdefault(lane, {}).setdefault(mode, 0)
        counts[lane][mode] += 1
filled = sum(1 for d in out.values() for v in d.values() for p in v[2] if p[4] == 2)

# Items tab: Emerald+ builds from Lolalytics (items/lol.tsv) and pro builds from pros.lol (items/pro.tsv), fetched 10 Nov 2026.
# B[lane][champ] = [wr, pick rate, games, start, boots, builds, 4th items, pro]
#   start = [[ids, share %]], boots = [[id, share %]], builds = [[full ids, wr of the first three, games, share %, most common, k]],
#   late = situational item ids
#   pro = [pro games, games used for item stats, [[id, % of games]], [[pro, team, win, kda, vs, ids]]] or 0
ITEMS = {}
for line in open(os.path.join(HERE, "items", "items.tsv"), encoding="utf-8"):
    i, name, _cat = line.rstrip("\n").split("\t")
    ITEMS[int(i)] = name
def ids(s):
    v = [int(x) for x in s.split("_") if x]
    for x in v:
        if x not in ITEMS:
            raise SystemExit(f"unknown item {x}")
    return v
B = {}
for line in open(os.path.join(HERE, "items", "lol.tsv"), encoding="utf-8"):
    f = line.rstrip("\n").split("\t")
    name, lane = canon(f[0]), f[1]
    start = [[ids(a), int(b)] for a, b in (x.split(":") for x in f[5].split(";") if x)]
    boots = [[ids(a)[0], int(b)] for a, b in (x.split(":") for x in f[6].split(";") if x)]
    builds = []
    for x in f[7].split(";"):
        a, wr, n, sh, common = x.split(":")
        builds.append([ids(a), float(wr), int(n), int(sh), int(common)])
    late = [[ids(a)[0], int(b)] for a, b in (x.split(":") for x in f[8].split(";") if x)]
    B.setdefault(lane, {})[name] = [float(f[2]), float(f[3]), int(f[4]), start, boots, builds, late, 0]
for line in open(os.path.join(HERE, "items", "pro.tsv"), encoding="utf-8"):
    f = line.rstrip("\n").split("\t")
    name, lane = canon(f[0]), f[1]
    cnt, used = int(f[2]), int(f[3])
    if cnt:
        top = [[ids(a)[0], min(100, int(b))] for a, b in (x.split(":") for x in f[4].split(";") if x)]
        games = []
        for g in filter(None, f[5].split("|")):
            pro, team, win, kda, vs, its = g.split(",")
            games.append([pro, team, int(win), kda, vs, ids(its)])
        B[lane][name][7] = [cnt, used, top, games]
# Full builds (items/full.tsv, fetched 10 Nov 2026 from the Lolalytics item-set data): each core above is extended item by item
# with what players who built exactly that start most often bought next, up to six items (bot lane: seven, the 7th by late-game popularity).
# Per build: ids after the core and k = how many items of the full build come from real item sequences (the rest by popularity).
# The last field lists other popular late items that are not in any of the three builds (situational picks).
for line in open(os.path.join(HERE, "items", "full.tsv"), encoding="utf-8"):
    f = line.rstrip("\n").split("\t")
    name, lane = canon(f[0]), f[1]
    e = B[lane][name]
    exts = f[2].split(";")
    if len(exts) != len(e[5]):
        raise SystemExit(f"build count mismatch {lane} {name}")
    for b, x in zip(e[5], exts):
        more, k = x.split(":")
        full = b[0] + ids(more)
        if len(set(full)) != len(full):
            raise SystemExit(f"duplicate item {lane} {name} {full}")
        want = 7 if lane == "bottom" else 6
        if len(full) not in (want, want - 1) and not (len(full) == 6 and lane == "bottom"):
            print("short build", lane, name, len(full))
        b[0] = full
        b.append(int(k))
    e[6] = ids(f[3].replace(";", "_"))
# Item tier list (items/slots.tsv): for every champion and lane, the win rate and games of each finished item completed as
# the 1st..5th item, and of boots. Items finished late always win more (they get finished mostly in won games), so an item
# is compared with the champion's other items finished in the same order: delta = games-weighted mean of
# (item win rate - average win rate of that slot), in percentage points. Boots are compared with other boots.
# Deltas are shrunk towards 0 by TIER_K games so that small samples stay in the middle tiers.
# Lane lists add up all champions in that lane. Only items bought in at least 1 % of the games are listed (champion lists:
# 1 % of that champion's games, at least 300 games). Mejai's Soulstealer (3041) is left out: it gets finished mostly when
# ahead; so are Slightly Magical Footwear (2422), free boots from a rune, not a purchase.
# T[lane] = {"a": items, "ab": boots, "c": {champ: items}, "cb": {champ: boots}}, entry = [id, delta*10, games, win rate*10, slot]
TIER_K, TIER_MIN_GAMES, TIER_SHARE = 1000, 300, 0.01
def tier_rows(groups):
    """groups: list of slot lists [(id, wr, n)]; returns {id: [n, sum n*delta, sum n*wr, {slot: n}]}."""
    acc = {}
    for si, rows in enumerate(groups):
        rows = [r for r in rows if r[0] not in (3041, 2422)]
        tot = sum(r[2] for r in rows)
        if not tot:
            continue
        avg = sum(r[1] * r[2] for r in rows) / tot
        for i, wr, n in rows:
            a = acc.setdefault(i, [0, 0.0, 0.0, {}])
            a[0] += n; a[1] += n * (wr - avg); a[2] += n * wr; a[3][si + 1] = a[3].get(si + 1, 0) + n
    return acc
def tier_out(acc, minn):
    res = []
    for i, (n, d, w, sl) in acc.items():
        if n < minn:
            continue
        if i not in ITEMS:
            raise SystemExit(f"unknown item {i}")
        delta = d / n * n / (n + TIER_K)
        res.append([i, round(delta * 10), n, round(w / n * 10), max(sl, key=sl.get)])
    res.sort(key=lambda r: (-r[1], -r[2]))
    return res
T, lane_acc = {}, {}
for line in open(os.path.join(HERE, "items", "slots.tsv"), encoding="utf-8"):
    f = line.rstrip("\n").split("\t")
    name, lane = canon(f[0]), f[1]
    parts = [[(int(a), float(b), int(c)) for a, b, c in (x.split(":") for x in p.split(",") if x)] for p in f[2].split("|")]
    if len(parts) != 6:
        raise SystemExit(f"bad slots line {lane} {name}")
    items_acc, boots_acc = tier_rows(parts[:5]), tier_rows([parts[5]])
    t = T.setdefault(lane, {"a": [], "ab": [], "c": {}, "cb": {}})
    games = B[lane][name][2]
    minn = max(TIER_MIN_GAMES, TIER_SHARE * games)
    t["c"][name], t["cb"][name] = tier_out(items_acc, minn), tier_out(boots_acc, minn)
    for key_, acc in (("a", items_acc), ("ab", boots_acc)):
        la = lane_acc.setdefault((lane, key_), {})
        for i, (n, d, w, sl) in acc.items():
            x = la.setdefault(i, [0, 0.0, 0.0, {}])
            x[0] += n; x[1] += d; x[2] += w
            for k_, v_ in sl.items():
                x[3][k_] = x[3].get(k_, 0) + v_
for (lane, key_), acc in lane_acc.items():
    T[lane][key_] = tier_out(acc, TIER_SHARE * sum(e[2] for e in B[lane].values()))
print("item tier list:", {lane: [len(T[lane]["a"]), len(T[lane]["ab"]), len(T[lane]["c"])] for lane in LANES})
nb = sum(len(v) for v in B.values())
print("builds:", nb, "with pro data:", sum(1 for v in B.values() for e in v.values() if e[7]))
# every recommended counter pick should have a build in that lane, so its "Build" button works
nobuild = sorted({(lane, p[0]) for lane, d in out.items() for e in d.values() for p in e[2] if p[0] not in B.get(lane, {})})
print("counter picks without a build in their lane:", len(nobuild), nobuild[:12])
from dd import DD, DD_VERSION
champs = [{"n": n, "c": M[n][0], "t": M[n][2], "i": DD[n]} for n in sorted(M, key=key)]
used_items = sorted({i for d in B.values() for e in d.values() for i in
    [x for s in e[3] for x in s[0]] + [b[0] for b in e[4]] + [x for b in e[5] for x in b[0]] + list(e[6]) +
    ([t[0] for t in e[7][2]] + [x for g in e[7][3] for x in g[5]] if e[7] else [])})
used_items = sorted(set(used_items) | {r[0] for t in T.values() for k_ in ("a", "ab") for r in t[k_]} |
                    {r[0] for t in T.values() for k_ in ("c", "cb") for rows in t[k_].values() for r in rows})
payload = {"dd": DD_VERSION, "champs": champs, "d": out, "g": G, "b": B, "t": T, "items": {i: ITEMS[i] for i in used_items}}
for lane in LANES:
    print(lane, len(out[lane]), counts[lane])
print("class-based picks in the lists:", filled)
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
assert tpl.count("/*__DATA__*/null") == 1
html = tpl.replace("/*__DATA__*/null", json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
# The template is a page fragment (Claude artifacts add the document shell). The website needs a full document.
head_end = html.index("</style>") + len("</style>")
head, body = html[:head_end], html[head_end:]
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
DESC = "Countery na každého championa podle Emerald+ dat, klikací matchupy a nejlepší buildy včetně pro hráčů."
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath d='M50 4 89 27v46L50 96 11 73V27z' fill='%23010a13' stroke='%23c8aa6e' stroke-width='6'/%3E"
        "%3Cpath d='M37 26h10v38h20l-6 10H37z' fill='%23c8aa6e'/%3E%3Cpath d='M58 34l7-8 7 8-7 8z' fill='%230ac8b9'/%3E%3C/svg%3E")
site = f"""<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{DESC}">
<meta property="og:title" content="Luban.GG">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#010a13">
<link rel="icon" href="{ICON}">
{head}
</head>
<body>{body}
</body>
</html>
"""
SITE = os.path.join(os.path.dirname(HERE), "docs", "index.html")
open(SITE, "w", encoding="utf-8").write(site)
print("champions:", len(champs), "site:", SITE, len(site.encode("utf-8")), "bytes")
# optional: also write the fragment for a Claude artifact, e.g. python3 src/build.py --artifact /path/page.html
if "--artifact" in sys.argv:
    dest = sys.argv[sys.argv.index("--artifact") + 1]
    open(dest, "w", encoding="utf-8").write(html)
    print("artifact copy:", dest, len(html.encode("utf-8")), "bytes")
