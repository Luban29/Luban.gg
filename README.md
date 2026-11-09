# Luban.GG

Countery a buildy pro League of Legends. Ke každému enemy na každé lince je deset counter picků podle Emerald+ dat
(Lolalytics, posledních 30 dní), u každého picku matchup s důvodem a v záložce Itemy nejlepší buildy pro Emerald+
a buildy pro hráčů (pros.lol).

Web: https://luban29.github.io/Luban.gg/

## Jak je projekt poskládaný

- `docs/index.html` je hotový web. GitHub Pages ho servíruje z větve `main`, složky `/docs`.
- `src/template.html` je vzhled a logika stránky, `src/build.py` do ní vloží data a zapíše `docs/index.html`.
- Úprava = změnit soubory v `src/`, spustit `python3 src/build.py`, commitnout a pushnout na `main`.
  GitHub Pages web obnoví zhruba do minuty.

## Data v `src/`

| Soubor | Co obsahuje |
| --- | --- |
| `e30/<linka>.tsv` | výběr counterů z Emerald+: enemy, režim (E, L, S, C, X), počet her, picky `Jméno:WR:hry` |
| `e30/more.tsv`, `e30/cls10.tsv` | další přímé matchupy a picky podle typu enemy, doplnění na deset picků |
| `e30/pools.txt` | championi, kteří se na lince opravdu hrají (pick rate a winrate na lince) |
| `e30/pr.txt` | pick rate enemy na linkách |
| `items/lol.tsv`, `items/full.tsv` | buildy z Lolalytics (Emerald+), plné buildy po šesti a sedmi itemech |
| `items/pro.tsv` | buildy pro hráčů z pros.lol |
| `items/items.tsv` | názvy itemů podle Data Dragon |
| `meta.py` | championi, jejich typ a tip na lajnu |
| `why.py`, `alt_why.py`, `reasons/`, `exc.py`, `e30/cls_why.py`, `e30/lane_why.py` | napsané důvody u counterů a popisy, jak picky hrají lajnu |

Data jsou stažená 7. a 8. 11. 2026. Procenta jsou winrate picku v daném matchupu, pokud stránka neříká jinak.

## Poznámka k právům

Luban.GG was created under Riot Games' "Legal Jibber Jabber" policy using assets owned by Riot Games.
Riot Games does not endorse or sponsor this project.
