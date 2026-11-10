"""Assemble data handed over by the collectors.

The browser tool saves results that are too long for the conversation into tool-results files. The collectors return
"CHUNK|name|i|payload|END" (LUBAN.get / PROS.get; short ones padded with "~" so they land in a file too).
Usage: python3 src/update/xfer.py NAME CHUNKS FNV LENGTH OUT  (CHUNKS, FNV and LENGTH as printed by LUBAN.put / PROS.put)
"""
import glob, json, os, sys
TR = os.path.expanduser("~/.claude/projects/")
def fnv(s):
    h = 0x811c9dc5
    for ch in s:
        h ^= ord(ch); h = (h * 0x01000193) & 0xffffffff
    return format(h, "x")
def chunks():
    out = {}
    for f in sorted(glob.glob(TR + "**/tool-results/*Browser__javascript_tool-*.txt", recursive=True), key=os.path.getmtime):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        t = "".join(x.get("text", "") for x in d if isinstance(x, dict))
        i = t.find('"')
        if i < 0: continue
        try:
            s, _ = json.JSONDecoder().raw_decode(t, i)
        except Exception:
            continue
        if not isinstance(s, str): continue
        s = s.rstrip("~")  # small results are padded so that they land in a file, not in the conversation
        if not s.startswith("CHUNK|") or not s.endswith("|END"): continue
        _, name, idx, rest = s.split("|", 3)
        out.setdefault(name, {})[int(idx)] = rest[:-4]
    return out
def assemble(name, n, want_fnv=None, want_len=None):
    c = chunks().get(name, {})
    missing = [i for i in range(n) if i not in c]
    if missing: raise SystemExit(f"{name}: missing chunks {missing}")
    s = "".join(c[i] for i in range(n))
    if want_len is not None and len(s) != want_len: raise SystemExit(f"{name}: length {len(s)} != {want_len}")
    if want_fnv and fnv(s) != want_fnv: raise SystemExit(f"{name}: fnv {fnv(s)} != {want_fnv}")
    return s
if __name__ == "__main__":
    name, n, f, ln, dest = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5]
    s = assemble(name, n, f, ln)
    open(dest, "w", encoding="utf-8").write(s)
    print(name, "ok", len(s), fnv(s), "->", dest)
