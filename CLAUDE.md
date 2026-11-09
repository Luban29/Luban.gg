# Luban.GG – pokyny pro Clauda

- Web je `docs/index.html` a GitHub Pages ho servíruje z větve `main`, složky `/docs`.
  Generuje ho `python3 src/build.py` ze `src/template.html` a dat v `src/`, `docs/index.html` se ručně needituje.
- Po každé změně spusť build a stránku zkontroluj v headless prohlížeči: countery pro všechny linky a championy
  (každý ze 10 picků se dá rozkliknout), záložku Itemy, žádný text `undefined`/`NaN` a žádný vodorovný scroll na 320 px.
- Texty na stránce jsou česky, tykání, s běžným herním slangem (top, jungle, mid, ADC, support, matchup, build).
- Data jsou z Lolalytics (jen Emerald+, posledních 30 dní) a pros.lol, názvy itemů z Data Dragon. Formáty souborů popisuje README.
  Když se data obnoví, uprav datum v patičkách v `src/template.html`.
- Patička musí dál obsahovat poznámku podle pravidel Riot Games „Legal Jibber Jabber“.
- Kopie pro artifact na claude.ai (fragment bez obalu dokumentu): `python3 src/build.py --artifact /cesta/stranka.html`.
