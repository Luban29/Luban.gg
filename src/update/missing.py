"""List what still needs writing after new counter data: reasons and lane descriptions.

Main counters (first pick in modes E, L, S) must have a written reason, the build stops without one.
Alternatives without a reason fall back to the pick's lane description, so writing them is nice but optional.
Every champion played in a lane needs a lane description in e30/lane_why.py.

Write reasons into a new file src/reasons/<lane>_<n>.txt, one per line: enemy|pick|why the pick beats the enemy
(Czech, short, from the champions' kits; "ho" for a male enemy, "ji" for a female one).
Usage: python3 src/update/missing.py
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
sys.path.insert(0, SRC)
sys.path.insert(0, os.path.join(SRC, "e30"))
from dump_missing import load_have
from sel import entries, POOLS
from lane_why import LANE_WHY

have = load_have()
main, alt = {}, {}
for lane, e, mode, tot, rows in entries():
    if mode not in "ELS":
        continue
    for i, (p, wr, g) in enumerate(rows):
        if (lane, e, p) not in have:
            (main if i == 0 else alt).setdefault(lane, []).append(f"{e}|{p}")
lanes = [(l, n) for l in POOLS for n in POOLS[l] if (l, n) not in LANE_WHY]
print("main picks without a reason (required):", sum(len(v) for v in main.values()))
for lane, v in main.items():
    print(f"  {lane}: " + "; ".join(v))
print("alternatives without a reason (optional):", sum(len(v) for v in alt.values()))
for lane, v in alt.items():
    print(f"  {lane}: " + "; ".join(v))
print("lane descriptions missing (required):", lanes)
