// Luban.GG data collector for Lolalytics: Emerald+, ranked solo/duo, last 30 days (patch=30).
// Run it in a lolalytics.com tab (Claude pastes it through the built-in browser of the Claude desktop app).
//   await LUBAN.meta()          champion names, ids and item names
//   LUBAN.counters()            raw counters for every champion and lane         -> LUBAN.out.raw
//   LUBAN.builds(queue)         builds and full builds for [[name, lane], ...]     -> LUBAN.out.lol, LUBAN.out.full
//   LUBAN.status()              progress of the running job
//   LUBAN.put(name, text) / LUBAN.get(name, i) hand results over in chunks of 200 000 characters with a checksum.
(() => {
// Pasting it again keeps data already collected in this tab (LUBAN.out) and replaces only the code.
const L = window.LUBAN = Object.assign(window.LUBAN || {}, {job: null});
L.out = L.out || {}; L.xfer = L.xfer || {};
const Q = {top: "top", jungle: "jungle", mid: "middle", bottom: "bottom", support: "support"};
const API = "https://a1.lolalytics.com/mega/?v=1&patch=30&tier=emerald_plus&queue=ranked&region=all";
const CHUNK = 200000;
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function json(url) {
  let err;
  for (let t = 0; t < 4; t++) {
    try {
      const r = await fetch(url);
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    } catch (e) { err = e; await sleep(800 * (t + 1)); }
  }
  throw err;
}

// q-data.json is Qwik's serialised state: values sit in _objs and objects/arrays refer to them by base-36 index.
L.qd = function (j) {
  const objs = j._objs, memo = new Map();
  function res(id) {
    if (typeof id !== "string") return id;
    const i = parseInt(id, 36);
    if (memo.has(i)) return memo.get(i);
    const v = objs[i];
    let out;
    if (Array.isArray(v)) { out = []; memo.set(i, out); for (const x of v) out.push(res(x)); return out; }
    if (v && typeof v === "object") { out = {}; memo.set(i, out); for (const k in v) out[k] = res(v[k]); return out; }
    if (typeof v === "string" && v.length && v.charCodeAt(0) < 32) {
      const c = v.charCodeAt(0);
      out = c === 1 ? undefined : (c >= 0x10 && c <= 0x12) ? res(v.slice(1).split(" ")[0]) : v;
    } else out = v;
    memo.set(i, out);
    return out;
  }
  return res(j._entry);
};

L.fnv = s => { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16); };
L.put = (name, s) => { L.xfer[name] = s; return {name, len: s.length, fnv: L.fnv(s), chunks: Math.ceil(s.length / CHUNK)}; };
L.get = (name, i) => "CHUNK|" + name + "|" + i + "|" + L.xfer[name].slice(i * CHUNK, (i + 1) * CHUNK) + "|END";

function start(name, tasks, workers, fn) {
  const job = L.job = {name, done: 0, total: tasks.length, errs: [], t0: Date.now()};
  const work = [...tasks];
  Promise.all(Array.from({length: workers}, async () => {
    while (work.length) {
      const x = work.shift();
      try { await fn(x); } catch (e) { job.errs.push(JSON.stringify(x) + ": " + e.message); }
      job.done++;
    }
  })).then(() => { job.t1 = Date.now(); });
  return {job: name, queued: tasks.length};
}
L.status = () => L.job && {job: L.job.name, done: L.job.done, total: L.job.total, finished: !!L.job.t1,
  secs: Math.round(((L.job.t1 || Date.now()) - L.job.t0) / 1000), errors: L.job.errs.length, firstErrors: L.job.errs.slice(0, 5)};

L.meta = async () => {
  const d = L.qd(await json("/lol/aatrox/build/q-data.json?lane=top&tier=emerald_plus&patch=30"));
  const g = Object.values(d.loaders).find(x => x && x.items && x.champions);
  L.champions = g.champions;      // slug -> name
  L.champPath = g.champPath;      // champion id -> slug
  L.itemNames = g.items;          // item id -> name
  L.patch = g.patch;
  return {patch: g.patch, champions: Object.keys(g.champions).length};
};

// Raw counters: for an enemy in a lane, its win rate against every champion it met in that lane (100+ games).
// Same shape as before: {slug, wr, pr, lanes, def, rows: [[name, enemy WR vs that champion, games, that champion's main lane]]}.
L.counters = () => {
  const tasks = [];
  for (const lane of Object.keys(Q)) for (const slug of Object.keys(L.champions)) tasks.push([lane, slug]);
  const raw = L.out.raw = {};
  return start("counters", tasks, 6, async ([lane, slug]) => {
    const j = await json(`${API}&ep=counter&c=${slug}&lane=${Q[lane]}`);
    const s = j.stats || {};
    const rows = (j.counters || []).map(c => [L.champions[L.champPath[c.cid]] || "#" + c.cid, c.vsWr, c.n, c.defaultLane])
      .sort((a, b) => b[1] - a[1]);
    raw[lane + "|" + L.champions[slug]] = {slug, wr: +s.wr || 0, pr: +s.pr || 0, lanes: s.lanes || {}, def: s.defaultLane || "", rows};
  });
};

// Which champion and lane combinations get builds: everyone really played in a lane (pick rate >= 1 %, or >= 0.5 % when
// the lane is at least a quarter of their games) plus every champion's main lane. Needs LUBAN.out.raw.
L.makeQueue = () => {
  const raw = L.out.raw, QL = {top: "top", jungle: "jungle", middle: "mid", bottom: "bottom", support: "support"};
  const pools = {}, def = {};
  for (const k in raw) {
    const [lane, n] = k.split("|"), d = raw[k];
    if (d.def) def[n] = d.def;
    if (d.pr >= 1 || (d.pr >= 0.5 && (d.lanes[Q[lane]] || 0) >= 25)) (pools[lane] = pools[lane] || []).push(n);
  }
  const queue = [];
  for (const n of Object.keys(def).sort()) {
    const ls = new Set();
    for (const l in pools) if (pools[l].includes(n)) ls.add(l);
    if (QL[def[n]]) ls.add(QL[def[n]]);
    for (const l of Object.keys(Q)) if (ls.has(l)) queue.push([n, l]);
  }
  return L.queue = queue;
};
// Raw counters sorted by key, ready for LUBAN.put("raw", ...).
L.rawText = () => { const o = {}; for (const k of Object.keys(L.out.raw).sort()) o[k] = L.out.raw[k]; return JSON.stringify(o); };

// Builds. Core builds are exact sets of the first three items incl. boots, grouped by the non-boot items and ranked
// by win rate minus 100/sqrt(games); the most common core always stays in. Full builds extend each core item by item
// with what players who built exactly that sequence bought next most often (item sequences from the build-itemset API),
// up to six items (bot lane seven); missing items are filled by late-game popularity. k = items backed by real sequences.
const BOOT_RE = /Boots|Greaves|Shoes|Treads|Steelcaps|Lucidity|Crushers|Armored Advance|Swiftmarch|Forever Forward/;
const r1 = x => Math.round(x * 10) / 10;
function extract(b, items) {
  const boots = new Set([1001, 9999]);
  b.boots.forEach(r => boots.add(r[0]));
  for (const id in items) if (BOOT_RE.test(items[id])) boots.add(+id);
  const G = new Map(); let tot = 0;
  for (const [ids, wr, pr, n] of b.builtBootSet3) {
    const a = ids.split("_").map(Number);
    const key = a.filter(x => !boots.has(x)).sort((x, y) => x - y).join("_");
    tot += n;
    let g = G.get(key);
    if (!g) { g = {key, n: 0, w: 0, best: null}; G.set(key, g); }
    g.n += n; g.w += n * wr / 100;
    if (!g.best || n > g.best.n) g.best = {ids: a, n};
  }
  const gs = [...G.values()].filter(g => g.key).map(g => ({...g, wr: 100 * g.w / g.n, share: 100 * g.n / tot}));
  gs.forEach(g => g.score = g.wr - 100 / Math.sqrt(g.n));
  const common = [...gs].sort((x, y) => y.n - x.n)[0];
  // cores built by at least 3 % of players; Mejai's Soulstealer (3041) cores are left out because their win rate is
  // inflated by players who only finish it when they are already winning
  const ok = g => !g.key.split("_").includes("3041");
  let pool = gs.filter(g => g.share >= 3 && ok(g));
  if (pool.length < 3) pool = gs.filter(g => g.share >= 1 && ok(g));
  if (pool.length < 3) pool = gs.filter(g => g.n >= 100 && ok(g));
  if (!pool.length) pool = gs;
  let pick = [...pool].sort((x, y) => y.score - x.score).slice(0, 3);
  if (common && !pick.includes(common)) { if (pick.length >= 3) pick[2] = common; else pick.push(common); }
  pick.sort((x, y) => y.score - x.score);
  const builds = pick.map(g => [g.best.ids.join("_"), r1(g.wr), g.n, Math.round(g.share), g === common ? 1 : 0].join(":")).join(";");
  // starting sets with at least 15 % of games, boots with at least 5 % (shares as whole percent)
  const start = b.startSet.filter(r => Math.round(r[2]) >= 15).slice(0, 2).map(r => r[0] + ":" + Math.round(r[2])).join(";");
  const bt = b.boots.filter(r => r[0] !== 1001 && r[0] !== 9999 && Math.round(r[2]) >= 5).slice(0, 3).map(r => r[0] + ":" + Math.round(r[2])).join(";");
  const i4 = b.item4.filter(r => !boots.has(r[0]));
  const s4 = i4.reduce((a, r) => a + r[3], 0) || 1;
  const late = [...i4].sort((x, y) => y[3] - x[3]).slice(0, 4).map(r => r[0] + ":" + Math.round(100 * r[3] / s4)).join(";");
  // late-game popularity: items bought 4th and 5th, by games
  const pop = new Map();
  for (const r of [...(b.item4 || []), ...(b.item5 || [])]) if (!boots.has(r[0])) pop.set(r[0], (pop.get(r[0]) || 0) + r[3]);
  return {line: [r1(b.header.wr), r1(b.header.pr), b.header.n, start, bt, builds, late].join("\t"),
    cores: pick.map(g => g.best.ids), pop: [...pop.entries()].sort((x, y) => y[1] - x[1]).map(x => x[0]), boots};
}
function fullBuilds(res, sets, lane) {
  const want = lane === "bottom" ? 7 : 6;
  const exts = res.cores.map(core => {
    const seq = core.slice();
    let k = seq.length;
    while (seq.length < 6) {
      const pre = seq.join("_") + "_", len = seq.length + 1;
      const next = (sets["itemBootSet" + len] || [])
        .filter(([ids]) => ids.startsWith(pre) && ids.split("_").length === len)
        .map(([ids, n]) => [+ids.split("_").pop(), n])
        .filter(([id]) => !seq.includes(id) && !res.boots.has(id))
        .sort((x, y) => y[1] - x[1])[0];
      if (!next) break;
      seq.push(next[0]);
      k = seq.length;
    }
    for (const id of res.pop) { if (seq.length >= want) break; if (!seq.includes(id)) seq.push(id); }
    return {seq, k};
  });
  const used = new Set(exts.flatMap(e => e.seq));
  const situational = res.pop.filter(id => !used.has(id)).slice(0, 4);
  return exts.map((e, i) => e.seq.slice(res.cores[i].length).join("_") + ":" + e.k).join(";") + "\t" + situational.join(";");
}
// Item tier list input: win rate and games of every finished item as the 1st to 5th item, and of boots
// ("id:wr:games" with 50+ games; slots separated by "|", boots last).
function slotLine(b) {
  const row = r => r[0] + ":" + r[1] + ":" + r[3];
  const slots = [b.item1, b.item2, b.item3, b.item4, b.item5].map(a => (a || []).filter(r => r[3] >= 50).map(row).join(","));
  const bt = (b.boots || []).filter(r => r[0] !== 1001 && r[0] !== 9999 && r[3] >= 50).map(row).join(",");
  return slots.join("|") + "|" + bt;
}
L.builds = queue => {
  const slug = {};
  for (const s in L.champions) slug[L.champions[s]] = s;
  L.out.lol = {}; L.out.full = {}; L.out.slots = {};
  return start("builds", queue, 3, async ([n, lane]) => {
    const d = L.qd(await json(`/lol/${slug[n]}/build/q-data.json?lane=${Q[lane]}&tier=emerald_plus&patch=30`));
    const b = Object.values(d.loaders).find(x => x && x.builtBootSet3);
    if (!b) throw new Error("no build data");
    const g = Object.values(d.loaders).find(x => x && x.items && x.champions);
    if (g) L.itemNames = g.items;
    const res = extract(b, L.itemNames);
    L.out.lol[n + "|" + lane] = res.line;
    L.out.slots[n + "|" + lane] = slotLine(b);
    const sets = (await json(`${API}&ep=build-itemset&c=${slug[n]}&lane=${Q[lane]}`)).itemSets || {};
    L.out.full[n + "|" + lane] = fullBuilds(res, sets, lane);
  });
};
return "LUBAN ready";
})();
