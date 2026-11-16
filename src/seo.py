"""Static pages for search engines: one page per enemy and lane with its ten counters, an index of them and a sitemap.

The interactive page is a single file that Google sees as one page. These small pages give every matchup its own address,
title and text (the same picks, win rates and reasons as the app) and link into the app with ?l=lane&c=champion.
Written to docs/counter/<lane>/<champion>/index.html, docs/counter/index.html and docs/sitemap.xml.
"""
import html, os, shutil
from urllib.parse import quote

BASE = "https://luban29.github.io/Luban.gg/"
LANE_URL = {"top": "top", "jungle": "jungle", "mid": "mid", "bottom": "adc", "support": "support"}
LANE_NAME = {"top": "top", "jungle": "jungle", "mid": "mid", "bottom": "ADC", "support": "support"}
LANE_PHRASE = {"top": "na topu", "jungle": "v jungli", "mid": "na midu", "bottom": "na botu", "support": "na supportu"}
CLS_NAME = {"tank": "tank", "bruiser": "bruiser", "assassin": "assassin", "mage": "mage", "adc": "střelec",
            "enchanter": "enchanter", "catcher": "engage support", "specialist": "specialista"}
VS_NOTE = {1: "winrate proti championům stejného typu", 2: "celkový winrate na lince"}

CSS = """:root{--bg:#010a13;--surface:#091428;--raise:#0f1e33;--line:#3c3221;--ink:#f0e6d2;--dim:#a09b8c;--gold:#c8aa6e;
--gold-deep:#785a28;--ally:#0ac8b9;--enemy:#d33f49;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(120% 60% at 50% 0%,#0a1a2e,#010a13 60%) fixed #010a13;color:var(--ink);
font:500 16px/1.5 "Barlow Semi Condensed","Arial Narrow",system-ui,sans-serif;padding:0 16px 40px}
main{max-width:640px;margin:0 auto}a{color:var(--gold)}
.top{display:flex;align-items:center;gap:10px;padding:16px 0;text-decoration:none;color:var(--ink);font:700 1.25rem Cinzel,Georgia,serif}
.top svg{width:34px;height:34px}.top em{font-style:normal;color:var(--gold)}
header.h{display:flex;align-items:center;gap:14px;padding:16px;border:1px solid var(--gold-deep);background:linear-gradient(104deg,#3a121980,#091428 70%)}
header.h img{width:72px;height:72px;border-radius:50%;border:2px solid var(--enemy);flex:none}
h1{margin:0;font:700 1.55rem/1.15 Cinzel,Georgia,serif}h1 small{display:block;font:600 .95rem "Barlow Semi Condensed",sans-serif;color:var(--dim);margin-top:4px}
h2{font:700 1.1rem Cinzel,Georgia,serif;margin:26px 0 10px;color:var(--gold)}
.lead{color:var(--dim)}
ol.p{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
ol.p li{display:grid;grid-template-columns:44px 1fr auto;gap:4px 12px;align-items:center;padding:10px 12px;border:1px solid var(--line);background:var(--surface)}
ol.p img{width:44px;height:44px;border-radius:50%;border:1.5px solid var(--ally);grid-row:span 2}
ol.p b{font-size:1.05rem}ol.p .wr{font-variant-numeric:tabular-nums;font-weight:700;color:var(--ally);text-align:right}
ol.p .wr.low{color:var(--enemy)}ol.p .why{grid-column:2/4;color:var(--dim);font-size:.95rem}
ol.p .g{display:block;font-size:.8rem;color:var(--dim);font-weight:500}
.tip{border-left:3px solid var(--gold);padding:10px 14px;background:var(--surface)}
.cta{display:inline-block;margin:22px 0 4px;padding:11px 18px;border:1px solid var(--gold);background:var(--raise);color:var(--gold);
font-weight:700;text-decoration:none}
.lanes,.idx{display:flex;flex-wrap:wrap;gap:6px;padding:0;list-style:none}.lanes a,.idx a{display:inline-block;padding:5px 10px;
border:1px solid var(--line);background:var(--surface);text-decoration:none;color:var(--ink)}
footer{margin-top:30px;color:var(--dim);font-size:.82rem}"""
LOGO = ('<svg viewBox="0 0 100 100" aria-hidden="true"><path d="M50 4 89 27v46L50 96 11 73V27z" fill="#010a13" stroke="#c8aa6e" '
        'stroke-width="5"/><path d="M37 26h10v38h20l-6 10H37z" fill="#c8aa6e"/><path d="M58 34l7-8 7 8-7 8z" fill="#0ac8b9"/></svg>')
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath d='M50 4 89 27v46L50 96 11 73V27z' "
        "fill='%23010a13' stroke='%23c8aa6e' stroke-width='6'/%3E%3Cpath d='M37 26h10v38h20l-6 10H37z' fill='%23c8aa6e'/%3E%3C/svg%3E")


def pct(x):
    return f"{x:.1f}".replace(".", ",") + " %"


def num(n):
    return f"{n:,}".replace(",", " ")


def page(title, desc, url, body, image=None):
    e = html.escape
    og = f'<meta property="og:image" content="{e(image)}">\n' if image else ""
    return f"""<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(url)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:type" content="article">
{og}<meta name="theme-color" content="#010a13">
<link rel="icon" href="{ICON}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Barlow+Semi+Condensed:wght@500;600;700&display=swap">
<style>{CSS}</style>
</head>
<body><main>
<a class="top" href="{BASE}">{LOGO}<span class="w">Luban<em>.GG</em></span></a>
{body}
<footer><p>Data z Lolalytics (Emerald+, posledních 30 dní). Luban.GG was created under Riot Games' "Legal Jibber Jabber" policy
using assets owned by Riot Games. Riot Games does not endorse or sponsor this project.</p></footer>
</main></body>
</html>
"""


def write(out, G, champs, dd_version, date, docs, key):
    e = html.escape
    ch = {c["n"]: c for c in champs}
    face = lambda n: f"https://ddragon.leagueoflegends.com/cdn/{dd_version}/img/champion/{ch[n]['i']}.png"
    root = os.path.join(docs, "counter")
    shutil.rmtree(root, ignore_errors=True)
    urls, index = [BASE, BASE + "counter/"], {}
    for lane, enemies in out.items():
        for name, (mode, pr, picks) in enemies.items():
            slug = key(name)
            rel = f"counter/{LANE_URL[lane]}/{slug}/"
            url = BASE + rel
            index.setdefault(lane, []).append((name, rel))
            top3 = ", ".join(f"{p[0]} {pct(p[1])}" for p in picks[:3])
            title = f"{name} {LANE_NAME[lane]} counter: 10 nejlepších picků (Emerald+) | Luban.GG"
            desc = (f"Nejlepší countery proti championovi {name} {LANE_PHRASE[lane]} podle Emerald+ her za 30 dní: {top3}. "
                    f"Proč fungují, buildy a tipy na lajnu.")
            items = []
            for p in picks:
                n, wr, games, why, kind, vs = p
                text = why or G.get(lane, {}).get(n, "")
                note = VS_NOTE.get(vs)
                games_txt = f"{num(games)} her" if games and vs == 0 else (note or "")
                if games and vs == 1:
                    games_txt = f"{num(games)} her, {note}"
                items.append(f'<li><img src="{e(face(n))}" alt="" width="44" height="44" loading="lazy"><b>{e(n)}</b>'
                             f'<span class="wr{" low" if vs != 2 and wr < 50 else ""}">{pct(wr)}<span class="g">{e(games_txt)}</span></span>'
                             f'<span class="why">{e(text)}</span></li>')
            others = "".join(f'<li><a href="{BASE}counter/{LANE_URL[l]}/{slug}/">{e(name)} {LANE_NAME[l]}</a></li>'
                             for l in out if l != lane and name in out[l])
            app = f"{BASE}?l={lane}&c={quote(name)}"
            body = f"""<header class="h"><img src="{e(face(name))}" alt="{e(name)}" width="72" height="72">
<h1>Counter na {e(name)} {LANE_NAME[lane]}<small>{e(CLS_NAME.get(ch[name]['c'], ''))}, {LANE_PHRASE[lane]}, data z {e(date)}</small></h1></header>
<p class="lead">Deset picků s nejlepším winratem proti championovi {e(name)} {LANE_PHRASE[lane]} v Emerald+ za posledních 30 dní, seřazené
od nejlepšího. U každého je důvod, proč v tomhle matchupu funguje.</p>
<ol class="p">{''.join(items)}</ol>
<h2>Tip na lajnu</h2><p class="tip">{e(ch[name]['t'])}</p>
<a class="cta" href="{e(app)}">Otevřít matchupy a buildy v Luban.GG</a>
{f'<h2>{e(name)} na jiných linkách</h2><ul class="lanes">{others}</ul>' if others else ''}
<p><a href="{BASE}counter/">Všechny countery</a></p>"""
            img = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{ch[name]['i']}_0.jpg"
            d = os.path.join(docs, rel)
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(title, desc, url, body, img))
            urls.append(url)
    lanes_html = "".join(
        f"<h2>{LANE_NAME[l].capitalize() if l != 'bottom' else 'ADC'}</h2><ul class=\"idx\">" +
        "".join(f'<li><a href="{BASE}{rel}">{e(n)}</a></li>' for n, rel in sorted(index[l], key=lambda x: key(x[0]))) + "</ul>"
        for l in out)
    body = f"""<h1>Countery na všechny championy<small>Emerald+ data za 30 dní, data z {e(date)}</small></h1>
<p class="lead">Vyber championa, proti kterému hraješ, a uvidíš deset nejlepších counter picků s důvody.</p>{lanes_html}"""
    os.makedirs(root, exist_ok=True)
    open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(
        page("Countery na všechny championy League of Legends (Emerald+) | Luban.GG",
             "Counter picky na všech 173 championů pro top, jungle, mid, ADC i support podle Emerald+ dat. Česky, s důvody a buildy.",
             BASE + "counter/", body))
    sm = "".join(f"<url><loc>{html.escape(u)}</loc></url>\n" for u in urls)
    open(os.path.join(docs, "sitemap.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
    return len(urls)
