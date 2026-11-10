// Luban.GG pro builds from pros.lol. Run it in a pros.lol tab (Claude pastes it through the built-in browser).
//   await PROS.meta()       champion names and pros.lol slugs
//   PROS.run(queue)         pro games for [[name, lane], ...]  -> PROS.out.pro
//   PROS.status(), PROS.put(name, text) / PROS.get(name, i) as in lolalytics.js
// Line per champion and lane: pro games, games used for item stats, items as id:% of games,
// three latest games as pro,team,win,k/d/a,vs champion,finished items, newest and oldest game timestamp.
(() => {
const P = window.PROS = Object.assign(window.PROS || {}, {job: null});
P.out = P.out || {}; P.xfer = P.xfer || {};
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
P.qd = function (j) {
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
P.fnv = s => { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16); };
P.put = (name, s) => { P.xfer[name] = s; return {name, len: s.length, fnv: P.fnv(s), chunks: Math.ceil(s.length / CHUNK)}; };
P.get = (name, i) => "CHUNK|" + name + "|" + i + "|" + P.xfer[name].slice(i * CHUNK, (i + 1) * CHUNK) + "|END";
P.status = () => P.job && {job: P.job.name, done: P.job.done, total: P.job.total, finished: !!P.job.t1,
  secs: Math.round(((P.job.t1 || Date.now()) - P.job.t0) / 1000), errors: P.job.errs.length, firstErrors: P.job.errs.slice(0, 5)};
P.meta = async () => {
  const d = P.qd(await json("/champion/aatrox/probuilds/q-data.json?lane=top"));
  const g = Object.values(d.loaders).find(v => v && v.champ && v.champPath);
  P.champ = g.champ;               // champion id -> name
  P.slug = {};                     // name -> pros.lol slug (nunu, renata, wukong, ...)
  for (const id in g.champ) P.slug[g.champ[id]] = g.champPath[id];
  return {champions: Object.keys(g.champ).length, patch: g.patch};
};
const clean = s => String(s == null ? "" : s).replace(/[,|\t\n]/g, " ").trim();
P.run = queue => {
  const pro = P.out.pro = {};
  const job = P.job = {name: "pros", done: 0, total: queue.length, errs: [], t0: Date.now()};
  const work = [...queue];
  Promise.all(Array.from({length: 3}, async () => {
    while (work.length) {
      const [n, lane] = work.shift();
      try {
        const slug = P.slug[n];
        if (!slug) throw new Error("unknown champion");
        const d = P.qd(await json(`/champion/${slug}/probuilds/q-data.json?lane=${lane}`));
        const D = (Object.values(d.loaders).find(v => v && v.data) || {}).data || {};
        const ms = D.matches || [];
        if (!D.count) { pro[n + "|" + lane] = "0\t0\t\t\t\t"; }
        else {
          const items = ((D.stats && D.stats.items) || []).map(([id, p]) => id + ":" + p).join(";");
          const games = ms.slice(0, 3).map(m => [clean(m.proName), clean(m.teamTag || m.teamName), m.win ? 1 : 0,
            `${m.kills}/${m.deaths}/${m.assists}`, clean(P.champ[m.vsChampion]), (m.fullItems || []).join("_")].join(",")).join("|");
          const ts = ms.map(m => m.timestamp).filter(Boolean);
          pro[n + "|" + lane] = [D.count, (D.stats && D.stats.statsCount) || 0, items, games,
            ts.length ? Math.max(...ts) : "", ts.length ? Math.min(...ts) : ""].join("\t");
        }
      } catch (e) { job.errs.push(n + "|" + lane + ": " + e.message); }
      job.done++;
    }
  })).then(() => { job.t1 = Date.now(); });
  return {job: "pros", queued: queue.length};
};
return "PROS ready";
})();
