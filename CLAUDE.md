# Luban.GG – pokyny pro Clauda

- Web je `docs/index.html` a GitHub Pages ho servíruje z větve `main`, složky `/docs`.
  Generuje ho `python3 src/build.py` ze `src/template.html` a dat v `src/`, `docs/index.html` se ručně needituje.
- Po každé změně spusť build a stránku zkontroluj v headless prohlížeči: countery pro všechny linky a championy
  (každý ze 10 picků se dá rozkliknout), záložku Itemy, žádný text `undefined`/`NaN` a žádný vodorovný scroll na 320 px.
- Texty na stránce jsou česky, tykání, s běžným herním slangem (top, jungle, mid, ADC, support, matchup, build).
- Data jsou z Lolalytics (jen Emerald+, posledních 30 dní) a pros.lol, názvy itemů z Data Dragon. Formáty souborů popisuje README.
- Patička musí dál obsahovat poznámku podle pravidel Riot Games „Legal Jibber Jabber“.
- Kopie pro artifact na claude.ai (fragment bez obalu dokumentu): `python3 src/build.py --artifact /cesta/stranka.html`.

## Aktualizace dat („aktualizuj luban.gg“)

Lolalytics ani pros.lol nejsou ze sandboxu dostupné, data se stahují přes vestavěný prohlížeč desktopové aplikace
Claude na počítači uživatele (nástroje `Claude_Browser`). Když prohlížeč není k dispozici, řekni to uživateli.

1. Otevři `https://lolalytics.com/lol/aatrox/build/?lane=top&tier=emerald_plus&patch=30` a přes `javascript_tool`
   vlož celý `src/collect/lolalytics.js`. Pak `await LUBAN.meta()` a `LUBAN.counters()`; průběh `LUBAN.status()` (asi 15 s).
2. `LUBAN.put("raw", LUBAN.rawText())` vrátí počet částí, délku a kontrolní součet. Každou část vyžádej
   `LUBAN.get("raw", i)`: dlouhý výsledek se uloží do souboru v tool-results a
   `python3 src/update/xfer.py raw ČÁSTI FNV DÉLKA raw.json` ho složí a ověří.
3. `python3 src/update/counters.py raw.json` přepíše soubory v `src/e30/` (výběr picků je stejný jako dřív,
   ze starých dat dává přesně původní soubory).
4. `LUBAN.builds(LUBAN.makeQueue())`, po doběhnutí
   `LUBAN.put("builds", JSON.stringify({lol: LUBAN.out.lol, full: LUBAN.out.full, slots: LUBAN.out.slots, items: LUBAN.itemNames, patch: LUBAN.patch}))`
   (`slots` jsou data pro tier list itemů)
   a přenos jako v kroku 2. Krátký výsledek doplň znaky „~“ (`LUBAN.get("builds", 0) + "~".repeat(160000)`), ať skončí v souboru.
5. Otevři `https://pros.lol/champion/aatrox/probuilds?lane=top`, vlož `src/collect/proslol.js`,
   `await PROS.meta()`, `PROS.run(fronta)` se stejnou frontou (`JSON.stringify(LUBAN.queue)` z lolalytics záložky),
   pak `PROS.put("pro", JSON.stringify(PROS.out.pro))` a přenos.
6. `python3 src/update/items.py builds.json pro.json` zapíše `src/items/`.
7. `python3 src/update/missing.py` vypíše chybějící texty. Hlavní countery a popisy lajn jsou povinné, alternativy
   bez důvodu dostanou popis lajny. Důvody piš do nového souboru `src/reasons/<linka>_<n>.txt` (`enemy|pick|proč`).
8. Uprav datum v patičkách `src/template.html`, v README a v komentářích `src/build.py`.
9. Build, kontrola stránky, commit a push. Po minutě ověř živý web na https://luban29.github.io/Luban.gg/.
