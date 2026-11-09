# Why each alternative works: "lane|enemy|alternative|sentence". Reasons come from champion kits.
RAW = """
top|Aatrox|Heimerdinger|Věžičky ho trestají při každém vstupu a granát přeruší jeho combo.
top|Aatrox|Sett|Vydrží jeho poke a W mu vrátí damage, který Sett dostal.
top|Aatrox|Singed|Kituje ho jedem a slowem, takže ho Aatrox nedohoní.
top|Ahri|Cho'Gath|Má tolik HP, že ho její burst nezabije, a Q ji chytí po dashi.
top|Ahri|Akali|Ve shroudu ji Ahri nevidí, takže charm těžko trefí, a zblízka ji Akali přebije.
top|Ahri|Irelia|Prodashuje se k ní přes miniony a zblízka ji přebije.
top|Akali|Kled|Vyhraje early all-in a Skaarl mu dá druhý život.
top|Akali|Sion|Má tolik HP, že ho její burst nezabije.
top|Akali|Irelia|Vyhrává dlouhé trady a stun ji chytí, jakmile vyleze ze shroudu.
top|Ambessa|Camille|Hookshot a true damage z Q vyhrávají krátké trady.
top|Ambessa|Irelia|Vyhrává dlouhé trady a stun ji zastaví mezi dashi.
top|Ambessa|Azir|Vojáci ji drží na distanci a R ji odhodí zpátky.
top|Anivia|Jax|Skočí přes zeď a v lajně ji přetlačí.
top|Anivia|Aatrox|Q dosáhne přes zeď a sustain ho drží v lajně.
top|Anivia|Kayle|Škáluje stejně dobře a v late game ji přeroste.
top|Camille|Ahri|Charm zastaví její vstup a z dálky ji pokuje.
top|Camille|Illaoi|Tentakly ji trestají, když skočí dovnitř.
top|Camille|Azir|Vojáci ji drží na distanci a R ji odhodí.
top|Cassiopeia|Sion|Vydrží její poke a škáluje HP.
top|Cassiopeia|K'Sante|Je odolný a R ji z dálky vytáhne k sobě.
top|Cho'Gath|Vayne|True damage z W prorazí jeho HP a z dálky ho kituje.
top|Cho'Gath|Aatrox|Q ho pokuje z dálky a sustain drží Aatroxe v lajně.
top|Cho'Gath|Kayle|Škáluje a v late game ho přeroste.
top|Darius|LeBlanc|Bursne ho z dálky a přes W se vrátí dřív, než ji pullne.
top|Darius|Wukong|Klon ho zmate a Wukong uteče z dosahu jeho Q.
top|Darius|Elise|Cocoon ho zastaví a z dálky ho pokuje.
top|Dr. Mundo|Aatrox|Q mu bere hodně HP a sustain drží Aatroxe v lajně.
top|Dr. Mundo|Warwick|Sustain vyhrává dlouhé trady a R ho chytí, když chce utéct.
top|Dr. Mundo|Irelia|Vyhrává dlouhé trady a % HP damage z itemů ho prorazí.
top|Fiora|Lissandra|Zmrazí ji z dálky a R zastaví její all-in.
top|Fiora|Ahri|Charm ji zastaví a z dálky ji pokuje.
top|Fiora|Quinn|Kituje ji z range a blind z Q jí zkazí trady.
top|Galio|Yone|Dává hlavně fyzický damage, proti kterému Galiův štít nepomůže.
top|Gangplank|Kayle|Škáluje a v late game ho přeroste.
top|Gangplank|Ornn|Vydrží jeho poke a itemy si staví přímo v lajně.
top|Gangplank|Quinn|Trestá ho early, než má itemy, a roamuje po mapě.
top|Garen|Camille|True damage z Q obchází jeho armor a hookshotem mu uteče z E.
top|Garen|Tryndamere|R ho drží naživu i přes Garenovo execute.
top|Garen|Darius|Bleed vyhrává dlouhé trady.
top|Gnar|Malphite|Armor tlumí jeho poke a R ho chytí.
top|Gnar|Kayle|Škáluje a v late game ho přeroste.
top|Gnar|Camille|Hookshot ji dostane k němu a v mini formě ji nezastaví.
top|Gragas|Singed|Proxy farmí a jedem ho trestá, když ho Gragas honí.
top|Gragas|Cho'Gath|Má tolik HP, že ho Gragasův poke neprorazí, a Q ho trestá za každý vstup.
top|Gragas|Zed|Pokuje ho přes stín a přes W uhne jeho E i barelu.
top|Gwen|Camille|True damage z Q ji bolí a E ji dostane přímo do mlhy.
top|Gwen|Garen|Silence přeruší její combo a W snižuje její damage.
top|Gwen|Sett|Je silný early a střed W dává true damage.
top|Heimerdinger|Syndra|Zničí věžičky z dálky a stun ho chytí.
top|Heimerdinger|Gangplank|Q ho pokuje z dálky a barely čistí věžičky.
top|Heimerdinger|Akali|Shroud ji kryje před věžičkami a burst ho zabije.
top|Illaoi|Mordekaiser|R ji odtrhne od tentaklů, které už má postavené.
top|Illaoi|Gangplank|Pokuje ji z dálky, kam tentakly nedosáhnou.
top|Illaoi|Gwen|Mlha ji chrání před Illaoiným E a zblízka ji v dlouhém duelu přebije.
top|Irelia|Warwick|Sustain vyhrává trady a R ji chytí i přes dashe.
top|Irelia|Jax|E zablokuje její autoattacky a na konci ji stunne.
top|Irelia|Shen|W zablokuje její autoattacky a taunt ji zastaví.
top|Jax|Poppy|W zastaví jeho skok a E ho přišpendlí ke zdi.
top|Jax|Singed|Flipne ho a proxy farmí, Jax ho nechytí.
top|Jax|Urgot|Vyhrává dlouhé trady a R ho na konci popraví.
top|Jayce|Ornn|Vydrží jeho poke a itemy si staví v lajně.
top|Jayce|Quinn|Kituje ho a blind z Q mu zkazí trady.
top|Jayce|Malzahar|Pasivní štít pohltí poke a R ho chytí.
top|K'Sante|Garen|R dává true damage a silence přeruší jeho combo.
top|K'Sante|Illaoi|Tentakly ho trestají v dlouhých tradech.
top|K'Sante|Singed|Proxy farmí a K'Sante ho nechytí.
top|Kalista|Jayce|Pokuje ji a knockback z E ji nepustí blízko.
top|Kayle|Malphite|Q ji early pokuje a R ji chytí.
top|Kayle|Yasuo|Wind wall blokuje její autoattacky a early ji trestá.
top|Kayle|Nasus|W ji zpomalí a Nasus škáluje stejně dobře jako ona.
top|Kennen|Ornn|Vydrží jeho poke a v teamfightu má silnější engage.
top|Kennen|Gangplank|Q ho pokuje a W ho očistí ze stunu.
top|Kennen|Dr. Mundo|Má HP a regeneraci, takže ho Kennenův poke neubije.
top|Kled|Fiora|W odrazí jeho Q a duel vyhraje.
top|Kled|Darius|Bleed vyhrává dlouhé trady.
top|Kled|Teemo|Blind mu zruší autoattacky a z dálky ho pokuje.
top|Malphite|Ornn|Vydrží jeho poke a itemy si staví v lajně.
top|Malphite|Sylas|Dává AP damage, se kterým armor nepomůže, a ukradne mu R.
top|Malphite|Dr. Mundo|Regenerace ho drží v lajně a % HP damage Malpha rozloží.
top|Malzahar|Tryndamere|R ho drží naživu i v suppressu.
top|Malzahar|Smolder|Pokuje ho z dálky a škáluje přes stacky.
top|Malzahar|Sion|Má tolik HP, že ho Malz neprorazí.
top|Maokai|Illaoi|Tentakly prorazí tanka v dlouhých tradech.
top|Maokai|Gwen|% HP damage ho rozloží i přes všechno HP.
top|Maokai|Mordekaiser|Dává AP damage a R ho izoluje od týmu.
top|Master Yi|Shen|W zablokuje jeho autoattacky a taunt ho zastaví.
top|Master Yi|Jax|E zablokuje jeho autoattacky a na konci ho stunne.
top|Master Yi|Sett|Je silný early a střed W dává true damage.
top|Mordekaiser|Singed|Utíká mu z Q a i v R ho jedem kituje.
top|Mordekaiser|Yone|Dashe uhýbají jeho Q a dlouhé trady vyhraje.
top|Mordekaiser|Gwen|% HP damage ho rozloží i přes jeho štít z W.
top|Nasus|Garen|Silence ho zastaví a je silný early, Nasus nestíhá stackovat.
top|Nasus|Renekton|Trestá ho early, takže Nasus nestíhá stackovat.
top|Nasus|Gangplank|Q ho pokuje a nedá mu v klidu farmit.
top|Olaf|Fiora|W odrazí jeho Q a duel vyhraje.
top|Olaf|Tryndamere|R ho drží naživu v Olafově all-inu.
top|Olaf|Trundle|R mu krade staty a pilíř ho zpomalí.
top|Ornn|Warwick|Sustain a % HP damage vyhrávají dlouhé trady.
top|Ornn|Kayle|Škáluje a v late game ho přeroste.
top|Ornn|Zed|Pokuje ho přes stín a z Ornnova engage uteče přes W.
top|Pantheon|Sion|Má tolik HP, že ho Panthův burst nezabije.
top|Pantheon|Gangplank|Q ho pokuje a GP škáluje lépe.
top|Pantheon|Olaf|Léčí se z W a R ho udělá imunním na Panthův stun.
top|Poppy|Darius|Bleed vyhrává dlouhé trady.
top|Quinn|Malphite|Armor a Q poke ji odradí a R ji chytí.
top|Quinn|Ornn|Vydrží její poke a v teamfightu engaguje.
top|Quinn|Dr. Mundo|Má HP a regeneraci, takže ho její poke neubije.
top|Renekton|Illaoi|Tentakly ho trestají v jeho all-inu.
top|Renekton|Lissandra|Zmrazí ho z dálky a R zastaví jeho all-in.
top|Renekton|Kayle|Škáluje a v late game ho přeroste.
top|Rengar|Garen|W snižuje damage z jeho skoku a silence ho zastaví.
top|Rengar|Yasuo|Wind wall blokuje jeho bolu a dashe mu dávají útěk.
top|Rengar|Irelia|Vyhrává dlouhé trady a stun ho chytí.
top|Riven|Garen|Silence přeruší její combo a W snižuje damage.
top|Riven|Renekton|Je silný early a stun přeruší její combo.
top|Riven|Gangplank|Q ji pokuje a W ho očistí ze stunu.
top|Rumble|Gangplank|Škáluje lépe a pokuje ho z dálky.
top|Rumble|Yone|Dashe ho dostanou z ohně a dlouhé trady vyhraje.
top|Rumble|Jax|Skočí na něj přes Q a duel vyhraje.
top|Ryze|Pantheon|Je silný early a stun ho chytí, Ryze je early slabý.
top|Ryze|Camille|Hookshot ji dostane k němu a true damage ho zabije.
top|Ryze|Akali|Bursne ho a ve shroudu ji Ryze nechytí.
top|Sett|Gnar|Kituje ho a v Mega formě ho přetlačí.
top|Sett|Anivia|Zeď ho zastaví a z dálky ho kituje.
top|Sett|Quinn|Kituje ho a nedá mu trade.
top|Shen|Zaahen|Sustain a revive mu dávají dlouhé trady.
top|Shen|Dr. Mundo|Dává % HP damage a regeneruje, Shen ho neprorazí.
top|Shen|Illaoi|Tentakly ho trestají v dlouhých tradech.
top|Singed|Teemo|Pokuje ho z dálky a houby ho trestají při proxy.
top|Singed|Urgot|E ho chytí a W ho rozstřílí, než uteče.
top|Singed|Fiora|% HP true damage ho rozloží a split mu odpoví na proxy.
top|Sion|Singed|Proxy farmí a Sion ho nechytí.
top|Sion|Yone|Dashe uhýbají jeho Q a dlouhé trady vyhraje.
top|Sion|Dr. Mundo|Dává % HP damage a regenerací vydrží jeho trady.
top|Swain|Gangplank|Q ho pokuje a W ho očistí z rootu.
top|Swain|Fiora|W odrazí jeho root a duel vyhraje.
top|Sylas|Kled|Je silný early a Skaarl mu dá druhý život.
top|Sylas|Sion|Má tolik HP, že ho Sylasův burst nezabije.
top|Sylas|Singed|Kituje ho a proxy farmí, Sylas ho nechytí.
top|Tahm Kench|Illaoi|Tentakly prorazí tanka v dlouhých tradech.
top|Tahm Kench|Aatrox|Sustain ho drží v lajně a Q trestá každý Tahmův vstup.
top|Tahm Kench|Darius|Bleed vyhrává dlouhé trady.
top|Teemo|Sion|Vydrží jeho poke a škáluje HP.
top|Trundle|Malphite|Armor tlumí jeho autoattacky a R ho chytí.
top|Trundle|Mordekaiser|Dává AP damage a R ho izoluje.
top|Trundle|Jax|E zablokuje jeho autoattacky.
top|Tryndamere|Darius|Bleed a pull ho přetlačí early.
top|Tryndamere|Zaahen|Sustain a revive, Trynd ho nedorazí.
top|Tryndamere|Singed|Flipne ho a jed ho trestá, když ho Trynd honí.
top|Urgot|Ornn|Vydrží jeho poke a itemy si staví v lajně.
top|Urgot|Illaoi|Tentakly ho trestají v dlouhých tradech.
top|Urgot|Mordekaiser|Dává AP damage a R ho izoluje.
top|Vayne|Teemo|Blind jí zruší autoattacky.
top|Vayne|Darius|Pull ji chytí a bleed ji zabije, než se rozjede.
top|Vayne|Sett|Je silný early a trestá ji, dokud nemá itemy.
top|Volibear|Renekton|Je silný early a stun přeruší jeho engage.
top|Volibear|Jayce|Pokuje ho a knockback z E ho odhodí.
top|Volibear|Shen|W zablokuje jeho autoattacky.
top|Warwick|Sett|Je silný early a střed W dává true damage.
top|Wukong|Illaoi|Tentakly ho trestají v jeho all-inu.
top|Wukong|Warwick|Sustain vyhrává trady a R ho chytí i přes klon.
top|Wukong|Akali|Dává AP burst a ve shroudu ji Wukong nechytí.
top|Yasuo|Renekton|Je silný early a stun přeruší jeho combo.
top|Yasuo|Darius|Bleed a pull ho přetlačí early.
top|Yasuo|Gangplank|Barely ho zasáhnou i přes wind wall.
top|Yone|Fiora|W odrazí jeho Q3 a duel vyhraje.
top|Yone|Irelia|Vyhrává dlouhé trady a stun ho chytí.
top|Yone|Jax|E zablokuje jeho autoattacky.
top|Yorick|Sion|Vydrží ghouly i Yoricka a v teamfightu má silnější engage.
top|Yorick|Renekton|Q čistí ghouly a early je silnější.
top|Yorick|Irelia|Dashuje po ghoulech až k Yorickovi.
top|Zaahen|Malphite|Armor tlumí jeho trady a R ho chytí.
top|Zaahen|Fiora|W odrazí jeho pull a % HP true damage ho zabije.
top|Zaahen|Singed|Kituje ho a Zaahen ho nechytí.
top|Zac|Illaoi|Tentakly prorazí tanka v dlouhých tradech.
top|Zac|Urgot|Vyhrává dlouhé trady a R ho na konci popraví.
top|Zac|Olaf|Je silný early a R ho drží v all-inu.
top|Zed|Nasus|W ho zpomalí a Nasus jeho burst vydrží.
top|Zed|Irelia|Vyhrává dlouhé trady a stun ho chytí.
top|Zed|Yasuo|Wind wall blokuje jeho shurikeny a dashe mu dávají útěk.
jungle|Amumu|Olaf|R ho dělá imunním na Amumuův stun.
jungle|Amumu|Talon|Ganguje rychle přes zdi a Amumu nestíhá reagovat.
jungle|Amumu|Jarvan IV|Je silný early a engage má rychlejší.
jungle|Bel'Veth|Kindred|Kituje ji a R jí zkazí all-in.
jungle|Bel'Veth|Lillia|Kituje ji, uspí ji a clearuje rychleji.
jungle|Bel'Veth|Sejuani|Vydrží její damage a CC ji zastaví.
jungle|Briar|Olaf|Vyhraje early duel a R ho drží v boji.
jungle|Briar|Jax|E zablokuje její autoattacky.
jungle|Briar|Ivern|Štíty a root ji zastaví, když se rozjede.
jungle|Cho'Gath|Lillia|Kituje ho a uspí, Cho ji nechytí.
jungle|Cho'Gath|Gwen|% HP damage ho rozloží i přes všechno HP.
jungle|Cho'Gath|Elise|Ganguje silně early a Cho je na to pomalý.
jungle|Darius|Zac|Má víc CC a engage, Darius se k nikomu nedostane.
jungle|Darius|Udyr|Vyhrává dlouhé duely a clearuje rychleji.
jungle|Darius|Nunu & Willump|Bere rychleji objektivy a ganguje dřív.
jungle|Dr. Mundo|Shyvana|% HP damage ho rozloží a clearuje rychleji.
jungle|Dr. Mundo|Talon|Ganguje rychle přes zdi a Mundo nestíhá.
jungle|Dr. Mundo|Lillia|Kituje ho a uspí ho.
jungle|Elise|Talon|Ganguje rychleji a bursne ji.
jungle|Elise|Shaco|Trestá ji early a krabice jí zastaví ganky.
jungle|Elise|Rammus|Vydrží její burst a tauntem ji zastaví.
jungle|Evelynn|Gwen|Vyhraje duel a mlha ji chrání.
jungle|Evelynn|Rek'Sai|Invaduje ji early, Eve je do šestky slabá.
jungle|Evelynn|Rengar|Vyhraje duel a invaduje ji early.
jungle|Fiddlesticks|Briar|Invaduje ho early, Fiddle je early slabý.
jungle|Fiddlesticks|Shyvana|Clearuje rychle a R ho dožene.
jungle|Fiddlesticks|Taliyah|Ganguje rychle a kamení ho drží od týmu.
jungle|Gragas|Master Yi|Škáluje a duely vyhraje.
jungle|Gragas|Hecarim|Ganguje rychle a engage má silnější.
jungle|Gragas|Shyvana|Clearuje rychle a škáluje.
jungle|Graves|Zyra|Rostliny ho zastaví a root ho chytí.
jungle|Graves|Sejuani|Vydrží jeho damage a CC ho zastaví.
jungle|Graves|Darius|Pull ho chytí a bleed vyhraje duel zblízka.
jungle|Gwen|Bel'Veth|Clearuje rychle a duel vyhraje.
jungle|Gwen|Viego|Je silný early a resety mu dávají skirmishe.
jungle|Gwen|Nidalee|Tlačí na ni early a kopím ji pokuje z dálky.
jungle|Hecarim|Cho'Gath|Vydrží jeho engage a knockup ho zastaví.
jungle|Hecarim|Darius|Pull ho chytí a bleed vyhraje duel.
jungle|Hecarim|Udyr|Vyhrává dlouhé duely.
jungle|Ivern|Zac|Má engage a CC, Ivern nemá čím se bránit.
jungle|Ivern|Fiddlesticks|Fear a burst ho zabijí, Ivern je squishy.
jungle|Ivern|Amumu|Q ho chytí a R stunne celý jeho tým, Ivern se nemá čím bránit.
jungle|Jarvan IV|Gragas|E přeruší jeho engage a odhodí ho.
jungle|Jarvan IV|Karthus|Škáluje a R zasáhne kohokoli.
jungle|Jarvan IV|Poppy|W zastaví jeho E+Q dash.
jungle|Jax|Rammus|Taunt ho zastaví a W mu vrací damage z autoattacků.
jungle|Jax|Zac|Má engage a CC, Jax ho early neprorazí.
jungle|Jax|Talon|Ganguje rychleji přes zdi, Jax nestíhá reagovat.
jungle|Karthus|Zyra|Rostliny a burst ho trestají a clearuje rychle.
jungle|Karthus|Cho'Gath|Vydrží jeho damage a CC ho zastaví.
jungle|Karthus|Evelynn|Bursne ho ze stealthu, Karthus je squishy.
jungle|Kayn|Zyra|Rostliny ho trestají a root ho chytí.
jungle|Kayn|Fiddlesticks|Fear a burst ho zastaví.
jungle|Kayn|Bel'Veth|Vyhraje duel a clearuje rychleji.
jungle|Kha'Zix|Skarner|Vydrží jeho burst a suppress ho chytí.
jungle|Kha'Zix|Rek'Sai|Invaduje ho early.
jungle|Kha'Zix|Ivern|Štíty a root mu kazí izolované killy.
jungle|Kindred|Briar|Invaduje ji early, Kindred je early slabá.
jungle|Kindred|Cho'Gath|Vydrží její damage a knockup ji zastaví.
jungle|Kindred|Ekko|Je mobilní a bursne ji.
jungle|Lee Sin|Elise|Je silná early a cocoon ho chytí.
jungle|Lee Sin|Shyvana|Škáluje a v late game ho přeroste.
jungle|Lee Sin|Ivern|Štíty a root mu kazí ganky.
jungle|Lillia|Kayn|Skočí na ni přes zdi a bursne ji.
jungle|Lillia|Zyra|Rostliny ji trestají a root ji chytí.
jungle|Lillia|Master Yi|V Q jí uhne a duel vyhraje.
jungle|Maokai|Ekko|Je mobilní a z Maokaiova engage uteče přes R.
jungle|Maokai|Master Yi|Škáluje a duely vyhraje.
jungle|Maokai|Shyvana|% HP damage ho rozloží a clearuje rychle.
jungle|Master Yi|Wukong|Klon a knockup ho zastaví.
jungle|Master Yi|Shaco|Krabice a fear ho zastaví.
jungle|Master Yi|Ivern|Root a štíty mu kazí resety.
jungle|Mordekaiser|Jarvan IV|Je silný early a engage s CC ho zastaví.
jungle|Mordekaiser|Sylas|Ukradne mu R a otočí ho proti němu.
jungle|Morgana|Shaco|Invaduje ji early.
jungle|Morgana|Talon|Ganguje rychle a bursne ji.
jungle|Morgana|Nocturne|R jí vypne vizi a skočí na ni.
jungle|Naafiri|Rammus|Vydrží její burst a W mu vrací damage od psů.
jungle|Naafiri|Wukong|Klon ji zmate a AoE knockup zasáhne i psy.
jungle|Naafiri|Kayn|Vyhraje duel a skočí na ni přes zdi.
jungle|Nidalee|Elise|Je silná early a cocoon ji chytí.
jungle|Nidalee|Evelynn|Bursne ji ze stealthu.
jungle|Nidalee|Fiddlesticks|Fear a burst ji zastaví.
jungle|Nocturne|Kha'Zix|Vyhraje duel a bursne ho.
jungle|Nocturne|Wukong|Klon ho zmate a knockup ho zastaví po jeho R.
jungle|Nocturne|Qiyana|Bursne ho a R ho omráčí.
jungle|Nunu & Willump|Fiddlesticks|Fear a burst ho zastaví a clearuje rychle.
jungle|Nunu & Willump|Cho'Gath|Vydrží jeho damage a CC ho zastaví.
jungle|Nunu & Willump|Zyra|Rostliny ho trestají a burst ho zabije.
jungle|Olaf|Graves|Kituje ho a bursne ho z dálky.
jungle|Olaf|Ekko|Je mobilní a bursne ho, Olaf ho nechytí.
jungle|Olaf|Sejuani|Vydrží jeho all-in a CC ho zastaví hned po R.
jungle|Pantheon|Wukong|Klon ho zmate a knockup ho chytí.
jungle|Pantheon|Hecarim|Ganguje rychle a engage má silnější.
jungle|Pantheon|Elise|Cocoon ho chytí a burst ho zabije.
jungle|Qiyana|Sion|Má tolik HP, že ho její burst nezabije.
jungle|Qiyana|Rammus|Vydrží její burst a tauntem ji zastaví.
jungle|Qiyana|Wukong|Klon ji zmate a knockup ji chytí.
jungle|Rammus|Lillia|Dává magic damage a kituje ho.
jungle|Rammus|Trundle|R mu krade armor a pilíř mu zastaví roll.
jungle|Rammus|Skarner|Vydrží jeho trady a suppress ho chytí.
jungle|Rek'Sai|Zyra|Rostliny a root ji zastaví.
jungle|Rek'Sai|Vi|R se nedá uhnout a early je silnější.
jungle|Rek'Sai|Hecarim|Ganguje rychle a engage má silnější.
jungle|Rengar|Kindred|Kituje ho a R mu zkazí burst.
jungle|Rengar|Naafiri|Psi a burst vyhrají duel.
jungle|Rengar|Master Yi|V Q mu uhne a duel vyhraje.
jungle|Sejuani|Rek'Sai|Invaduje ji early.
jungle|Sejuani|Zac|Vydrží její engage a vlastní má silnější.
jungle|Sejuani|Briar|Je silná early a invaduje ji.
jungle|Shaco|Karthus|AoE damage zabije klon i krabice.
jungle|Shaco|Ivern|Štíty a root ho zastaví.
jungle|Shaco|Nunu & Willump|Vydrží jeho burst a rychle bere objektivy.
jungle|Shyvana|Lillia|Kituje ji a uspí.
jungle|Shyvana|Cho'Gath|Vydrží její damage a knockup ji zastaví.
jungle|Shyvana|Bel'Veth|V přímém duelu ji přetlačí.
jungle|Skarner|Zyra|Rostliny a root ho zastaví.
jungle|Skarner|Gwen|% HP damage ho rozloží i přes tankiness.
jungle|Skarner|Warwick|Sustain mu dá vyhrát duel.
jungle|Sylas|Wukong|Klon a knockup ho chytí.
jungle|Sylas|Graves|Kituje ho a bursne ho.
jungle|Sylas|Kha'Zix|Bursne ho, když je izolovaný.
jungle|Taliyah|Aatrox|Diveuje ji a sustain ho drží v boji, Taliyah je squishy.
jungle|Taliyah|Zed|Je mobilní a bursne ji.
jungle|Taliyah|Rengar|Bursne ji z bushe.
jungle|Talon|Rammus|Vydrží jeho burst a tauntem ho zastaví.
jungle|Talon|Sion|Má tolik HP, že ho Talonův burst nezabije.
jungle|Talon|Bel'Veth|V přímém duelu ho přetlačí.
jungle|Trundle|Shyvana|% HP damage ho rozloží a clearuje rychleji.
jungle|Trundle|Graves|Kituje ho a bursne ho.
jungle|Trundle|Briar|Je silná early a duel vyhraje.
jungle|Udyr|Gragas|E ho odhodí a kituje ho.
jungle|Udyr|Wukong|Klon ho zmate a knockup ho chytí.
jungle|Udyr|Sejuani|Vydrží jeho damage a CC ho zastaví.
jungle|Vi|Wukong|Klon ji zmate a knockup ji chytí.
jungle|Vi|Master Yi|Škáluje a duely vyhraje.
jungle|Vi|Cho'Gath|Vydrží její burst a knockup ji zastaví.
jungle|Viego|Rammus|Tauntem ho zastaví a W mu vrací damage.
jungle|Viego|Bel'Veth|V přímém duelu ho přetlačí.
jungle|Viego|Evelynn|Bursne ho ze stealthu.
jungle|Volibear|Bel'Veth|Vyhraje dlouhý duel a dashe jí dávají útěk.
jungle|Volibear|Rammus|Vydrží jeho all-in a tauntem ho zastaví.
jungle|Volibear|Jarvan IV|Má silnější engage a víc CC.
jungle|Warwick|Shen|W blokuje jeho autoattacky a taunt ho zastaví.
jungle|Warwick|Morgana|Black Shield ruší jeho R a root ho chytí.
jungle|Warwick|Ivern|Štíty chrání spoluhráče a root ho zastaví.
jungle|Wukong|Dr. Mundo|Vydrží jeho burst a regenerací se vrátí do hry.
jungle|Wukong|Shyvana|% HP damage ho rozloží a clearuje rychle.
jungle|Wukong|Lillia|Kituje ho a uspí.
jungle|Xin Zhao|Amumu|Vydrží jeho damage a CC ho zastaví.
jungle|Xin Zhao|Ekko|Je mobilní a bursne ho.
jungle|Xin Zhao|Shyvana|Škáluje a % HP damage ho rozloží.
jungle|Zaahen|Kindred|Kituje ho a R ji drží naživu v duelu.
jungle|Zaahen|Kha'Zix|Bursne Zaahena, když je izolovaný.
jungle|Zaahen|Shaco|Invaduje ho early.
jungle|Zac|Ekko|Je mobilní a ze Zacova engage uteče přes R.
jungle|Zac|Taliyah|E ho stunne, když skáče přes kamení, a ganguje rychle.
jungle|Zac|Xin Zhao|Je silný early a duel vyhraje.
jungle|Zed|Gwen|Mlha ji chrání a duel vyhraje.
jungle|Zed|Wukong|Klon ho zmate a knockup ho chytí.
jungle|Zed|Rammus|Vydrží jeho burst a tauntem ho zastaví.
jungle|Zyra|Bel'Veth|Clearuje rychle a duel vyhraje.
jungle|Zyra|Rengar|Bursne ji z bushe.
jungle|Zyra|Ivern|Štíty chrání spoluhráče a root ji zastaví.
mid|Ahri|Dr. Mundo|Má tolik HP a regenerace, že ho její burst nezabije.
mid|Ahri|Sion|Má tolik HP, že ho její burst nezabije.
mid|Ahri|Fiora|W odrazí charm a v duelu ji přebije.
mid|Akali|Lissandra|Zmrazí ji a R zastaví její all-in.
mid|Akali|Taliyah|E ji stunne při dashi a W ji odhodí.
mid|Akali|Heimerdinger|Věžičky ji trestají, kdykoli vyleze ze shroudu, a E ji stunne.
mid|Akshan|Ekko|Bursne ho a W stun mu nedá utéct.
mid|Akshan|Katarina|Resety a mobilita jí dávají výhodu, Akshan ji nechytí.
mid|Akshan|Hwei|Má delší poke range a víc CC.
mid|Anivia|Zilean|Bomby ji pokují z dálky a revive ho drží naživu.
mid|Anivia|Ziggs|Má delší poke range a čistí vlnu rychleji.
mid|Anivia|Vel'Koz|Má delší poke range.
mid|Annie|Ekko|Je mobilní a R ho vrátí z jejího burstu.
mid|Annie|Anivia|Má delší range a zeď ji drží od těla.
mid|Annie|Veigar|Klec ji zastaví a v late game ji přeroste.
mid|Aurelion Sol|Fizz|E mu uhne a burst ho zabije, ASol je early slabý.
mid|Aurelion Sol|Zed|Bursne ho early, než ASol nastackuje.
mid|Aurelion Sol|Ahri|Charm ho chytí a díky mobilitě ho trestá early.
mid|Aurora|Zed|Bursne ji dřív, než stihne odskočit.
mid|Aurora|Vex|Pasiv ji trestá za každý skok.
mid|Aurora|Zoe|Má delší poke a bublina ji uspí.
mid|Azir|Syndra|Bursne ho a stun ho chytí, Azir je early slabý.
mid|Azir|Twisted Fate|Stunne ho kartou a roamuje po mapě.
mid|Azir|Diana|Skočí na něj a bursne ho.
mid|Cassiopeia|Vel'Koz|Má delší poke range.
mid|Cassiopeia|Zed|Je mobilnější a bursne ji.
mid|Cassiopeia|Malzahar|Pasivní štít pohltí poke a R ji chytí.
mid|Corki|Zoe|Uspí ho a pokuje ho z dálky.
mid|Corki|Lissandra|Zmrazí ho a R zastaví jeho all-in.
mid|Corki|Viktor|Má delší poke a čistí vlnu rychleji.
mid|Diana|Gwen|Mlha ji chrání a duel vyhraje.
mid|Diana|Mordekaiser|R ji izoluje a duel vyhraje.
mid|Diana|Ekko|Je mobilní a R ho vrátí z jejího all-inu.
mid|Ekko|Tryndamere|R ho drží naživu přes Ekkův burst.
mid|Ekko|Gragas|E ho odhodí a pokuje ho z dálky.
mid|Ekko|Quinn|Kituje ho a blind mu zkazí trady.
mid|Fizz|Lissandra|Zmrazí ho a R ho zastaví.
mid|Fizz|Diana|Vyhraje duel a R ho chytí.
mid|Fizz|Singed|Vydrží jeho burst a flipne ho.
mid|Galio|Vel'Koz|Má delší poke range.
mid|Galio|Neeko|Pokuje ho a R omráčí celý jeho tým.
mid|Galio|Gangplank|Q ho pokuje fyzickým damagem, proti kterému Galiův štít nepomůže.
mid|Hwei|Akshan|Je mobilní a bursne ho.
mid|Hwei|Katarina|Resety a mobilita, Hwei ji nechytí.
mid|Hwei|Xerath|Má delší poke range.
mid|Irelia|Locke|Bursne ji a R ji popraví.
mid|Irelia|Viktor|Pokuje ji a W ji zastaví.
mid|Irelia|LeBlanc|Bursne ji a odskočí dřív, než Irelia odpoví.
mid|Kassadin|Zed|Trestá ho early burstem.
mid|Kassadin|Talon|Trestá ho early a roamuje.
mid|Kassadin|Garen|Silence ho zastaví a W snižuje jeho damage.
mid|Katarina|Vex|Trestá její skoky.
mid|Katarina|Garen|Silence přeruší její R.
mid|Katarina|Vladimir|Léčí se a bazénem se vyhne jejímu R.
mid|LeBlanc|Vex|Trestá její skoky.
mid|LeBlanc|Twisted Fate|Stunne ji kartou a čistí vlnu rychleji.
mid|LeBlanc|Vladimir|Léčí se a bazénem se vyhne jejímu burstu.
mid|Lissandra|Akshan|Je mobilní a pokuje ji.
mid|Lissandra|Swain|Léčí se a root ji chytí, Lissandra ho nezabije.
mid|Lissandra|Xerath|Má delší poke range.
mid|Locke|Katarina|Resety a mobilita, Locke ji nechytí.
mid|Locke|Kassadin|Magický štít pohltí jeho burst a blinkem uteče.
mid|Locke|Akshan|Je mobilní a pokuje ho.
mid|Malzahar|Karthus|Pokuje ho AoE skilly a v late game ho přeroste.
mid|Malzahar|Hwei|Má delší poke range.
mid|Malzahar|Tryndamere|R ho drží naživu i v suppressu.
mid|Mel|Syndra|Její skilly nejsou projektily a stun Mel chytí.
mid|Mel|Cho'Gath|Q není projektil, takže ho Mel neodrazí, a vydrží její poke.
mid|Mel|Fizz|E jí uhne a burst ji zabije.
mid|Orianna|Vel'Koz|Má delší poke range.
mid|Orianna|LeBlanc|Bursne ji a odskočí.
mid|Orianna|Xerath|Má delší poke range.
mid|Ryze|Yasuo|Wind wall blokuje jeho Q.
mid|Ryze|Twisted Fate|Stunne ho kartou a roamuje.
mid|Ryze|Aurelion Sol|Pokuje ho a škáluje lépe.
mid|Sylas|Taliyah|Kamení ho trestá za skoky.
mid|Sylas|Tryndamere|R ho drží naživu přes Sylasův burst.
mid|Sylas|Singed|Vydrží jeho burst a kituje ho.
mid|Syndra|Fizz|E jí uhne a burst ji zabije.
mid|Syndra|Locke|Bursne ji a R ji popraví.
mid|Syndra|Zed|Je mobilnější a bursne ji.
mid|Taliyah|Katarina|Resety a mobilita, Taliyah ji nechytí.
mid|Taliyah|Zed|Je mobilnější a bursne ji.
mid|Taliyah|Annie|Stunne ji a bursne.
mid|Twisted Fate|Gwen|V mlze ji jeho karta nezasáhne a zblízka ho zabije.
mid|Twisted Fate|Locke|Bursne ho a R ho popraví.
mid|Twisted Fate|Fizz|Je mobilní a bursne ho.
mid|Veigar|Gwen|Mlha ji chrání a zblízka ho zabije.
mid|Veigar|Kassadin|Pasivně snižuje magický damage a štít z Q pohltí jeho burst.
mid|Veigar|Syndra|Má delší range a stunne ho.
mid|Vex|Vladimir|Nepotřebuje dashe, takže na něj její pasiv nefunguje, a bazénem se vyhne burstu.
mid|Vex|Malzahar|Pasivní štít pohltí poke a R ji chytí.
mid|Viktor|Xerath|Má delší poke range.
mid|Viktor|Aurelion Sol|Pokuje ho a škáluje lépe.
mid|Viktor|Vel'Koz|Má delší poke range.
mid|Vladimir|Anivia|Zeď ho drží od těla a škáluje stejně dobře.
mid|Vladimir|Aurora|Je mobilní a pokuje ho.
mid|Vladimir|Kog'Maw|% HP damage z range ho rozloží.
mid|Xerath|Gwen|Mlha ji chrání a zblízka ho zabije.
mid|Xerath|Katarina|Resety a mobilita, Xerath ji nechytí.
mid|Xerath|Aurora|Je mobilní a bursne ho.
mid|Yasuo|Singed|Vydrží jeho damage a flipne ho.
mid|Yasuo|Tryndamere|R ho drží naživu a duel vyhraje.
mid|Yasuo|Sett|Je silný early a střed W dává true damage.
mid|Zed|Diana|Vyhraje duel a štít pohltí jeho burst.
mid|Zed|Xerath|Má delší poke range.
mid|Zed|Fizz|E mu uhne a burst ho zabije.
mid|Zoe|Malzahar|Pasivní štít pohltí poke a R ji chytí.
mid|Zoe|Vex|Trestá její skoky.
mid|Zoe|Ekko|Je mobilní a bursne ji.
bottom|Aphelios|Swain|Léčí se z poke a root ho chytí, Aphelios nemá únik.
bottom|Aphelios|Yasuo|Wind wall blokuje jeho autoattacky.
bottom|Aphelios|Jinx|Škáluje a v teamfightu ho přeroste.
bottom|Ashe|Vel'Koz|Má delší poke range.
bottom|Ashe|Karthus|Pokuje ji AoE skilly a R ji zasáhne odkudkoli.
bottom|Ashe|Katarina|Resety a mobilita, Ashe ji nechytí.
bottom|Caitlyn|Vel'Koz|Má delší poke range.
bottom|Caitlyn|Karthus|Pokuje ji AoE skilly a R ji zasáhne odkudkoli.
bottom|Caitlyn|Xerath|Má delší poke range.
bottom|Corki|Kog'Maw|Má range a % HP damage.
bottom|Corki|Sivir|Štít blokuje jeho poke.
bottom|Corki|Xayah|Root ho chytí a během R je nezasažitelná.
bottom|Draven|Kog'Maw|Má delší range a škáluje lépe.
bottom|Draven|Yasuo|Wind wall blokuje jeho sekyry.
bottom|Draven|Xayah|Během R uhne jeho all-inu a root ho chytí.
bottom|Ezreal|Sivir|Štít blokuje jeho poke.
bottom|Ezreal|Katarina|Resety a mobilita, Ezreal ji nechytí.
bottom|Ezreal|Hwei|Má delší poke range.
bottom|Jhin|Master Yi|V Q mu uhne a duel vyhraje.
bottom|Jhin|Zeri|Je mobilní a škáluje lépe.
bottom|Jhin|Yasuo|Wind wall blokuje jeho střely.
bottom|Jinx|Vel'Koz|Má delší poke range.
bottom|Jinx|Syndra|Stunne ji a bursne.
bottom|Jinx|Hwei|Má delší poke range.
bottom|Kai'Sa|Karthus|Pokuje ji AoE skilly a R ji zasáhne odkudkoli.
bottom|Kai'Sa|Swain|Léčí se z poke a root ji chytí.
bottom|Kai'Sa|Nilah|W blokuje její autoattacky.
bottom|Kalista|Jinx|Škáluje a má delší range.
bottom|Kalista|Kog'Maw|Má delší range a škáluje lépe.
bottom|Kalista|Samira|W blokuje její kopí.
bottom|Kog'Maw|Vel'Koz|Má delší poke range.
bottom|Kog'Maw|Hwei|Má delší poke range.
bottom|Kog'Maw|Veigar|Klec ho chytí a burst ho zabije.
bottom|Lucian|Karthus|Pokuje ho AoE skilly a R ho zasáhne odkudkoli.
bottom|Lucian|Brand|AoE poke a burn ho rozloží.
bottom|Lucian|Taliyah|Kamení ho trestá za dash.
bottom|Miss Fortune|Xerath|Má delší poke range.
bottom|Miss Fortune|Ekko|Bursne ji a W stun přeruší její R.
bottom|Miss Fortune|Veigar|Klec ji chytí a burst ji zabije.
bottom|Nilah|Syndra|Stunne ji a bursne z dálky.
bottom|Nilah|Swain|Léčí se a root ji chytí.
bottom|Nilah|Veigar|Klec ji chytí a burst ji zabije.
bottom|Samira|Corki|Pokuje ji z delšího range.
bottom|Samira|Viktor|Pokuje ji a W zóna ji zastaví.
bottom|Samira|Xayah|Během R jí uhne a root ji chytí.
bottom|Sivir|Yunara|Škáluje a kituje ji.
bottom|Sivir|Zeri|Je mobilní a škáluje lépe.
bottom|Sivir|Aurelion Sol|Pokuje ji AoE skilly a v late game ji přeroste.
bottom|Smolder|Miss Fortune|Je silná early a pokuje ho.
bottom|Smolder|Zeri|Je mobilní a kituje ho.
bottom|Smolder|Kog'Maw|Má range a % HP damage.
bottom|Tristana|Draven|Je silný early a all-in vyhraje.
bottom|Tristana|Xayah|Během R uhne jejímu skoku a root ji chytí.
bottom|Tristana|Lucian|Je silný early a burst vyhraje.
bottom|Twitch|Karthus|Pokuje ho AoE skilly a R ho zasáhne i ve stealthu.
bottom|Twitch|Yasuo|Wind wall blokuje jeho autoattacky.
bottom|Twitch|Katarina|Resety a mobilita, Twitch ji nechytí.
bottom|Varus|Aphelios|Škáluje a v teamfightu ho přeroste.
bottom|Varus|Samira|W blokuje jeho Q.
bottom|Varus|Twitch|Ze stealthu ho dostihne, Varus nemá únik.
bottom|Vayne|Xayah|Root ji chytí a během R jí uhne z condemnu.
bottom|Vayne|Kog'Maw|Má range a % HP damage.
bottom|Vayne|Aurelion Sol|Pokuje ji AoE skilly a v late game ji přeroste.
bottom|Xayah|Viktor|Pokuje ji a W zóna ji zastaví.
bottom|Xayah|Ziggs|Má delší poke range.
bottom|Xayah|Swain|Léčí se a root ji chytí.
bottom|Yunara|Vel'Koz|Má delší poke range.
bottom|Yunara|Cassiopeia|Pokuje ji z dálky a W ji uzemní, takže neuteče.
bottom|Yunara|Syndra|Stunne ji a bursne.
bottom|Zeri|Draven|Je silný early a all-in vyhraje.
bottom|Zeri|Xayah|Root ji chytí a během R je nezasažitelná.
bottom|Zeri|Nilah|W blokuje její autoattacky.
bottom|Ziggs|Yasuo|Wind wall blokuje jeho bomby.
bottom|Ziggs|Vladimir|Léčí se a v bazénu se mu vyhne, Ziggs ho neprorazí.
bottom|Ziggs|Katarina|Resety a mobilita, Ziggs ji nechytí.
support|Alistar|Seraphine|Pokuje ho z dálky a stun ho zastaví.
support|Alistar|Poppy|W zastaví jeho dash.
support|Alistar|Soraka|Léčí spoluhráče a silence zastaví jeho combo.
support|Bard|Janna|Disengage a poke, Bard nemá jak engagovat.
support|Bard|Blitzcrank|Hookne ADC, když Bard roamuje.
support|Bard|Zilean|Bomby ho pokují a revive drží ADC naživu.
support|Blitzcrank|Zilean|Revive a slow mu zkazí každý hook.
support|Blitzcrank|Braum|Štítem blokuje hook.
support|Blitzcrank|Leona|Otočí jeho hook vlastním engagem.
support|Brand|Janna|Štíty a disengage, Brand ji neprorazí.
support|Brand|Zilean|Revive a bomby, Brand ho neprorazí.
support|Brand|Milio|Léčí z poke a R čistí CC z jeho stunu.
support|Braum|Senna|Pokuje ho z dálky, kam štít nestačí.
support|Braum|Rakan|Je mobilní a engagne mimo jeho štít.
support|Braum|Vel'Koz|Má delší poke range.
support|Janna|Amumu|Stunne ji přes Q a R chytí celý bot.
support|Karma|Sona|Léčí a pokuje, Karma ji neutáhne.
support|Karma|Nautilus|Hookne ji a engage vyhraje.
support|Karma|Blitzcrank|Hookne ji, když stojí mimo miniony.
support|Leona|Soraka|Léčí spoluhráče a silence zastaví její engage.
support|Lulu|Blitzcrank|Hookne ji, když stojí mimo miniony.
support|Lulu|Vel'Koz|Má delší poke range.
support|Lulu|Janna|Disengage a poke, Lulu nemá jak vyhrát trade.
support|Lux|Janna|Štíty a disengage, Lux nemá co trefit.
support|Lux|Blitzcrank|Hookne ji, když stojí mimo miniony.
support|Lux|Nami|Léčí a bublina ji chytí.
support|Maokai|Milio|R čistí CC z jeho engage.
support|Maokai|Thresh|Hook a lantern otočí jeho engage.
support|Milio|Janna|Pokuje ho a disengage drží ADC v bezpečí.
support|Milio|Blitzcrank|Hookne ho, když stojí mimo miniony.
support|Milio|Soraka|Léčí víc a silence zastaví engage.
support|Morgana|Milio|Léčí a čistí její root.
support|Morgana|Nami|Léčí a bublina ji chytí.
support|Morgana|Janna|Disengage a poke, Morgana nemá jak engagovat.
support|Nami|Blitzcrank|Hookne ji, když stojí mimo miniony.
support|Nami|Leona|All-in zblízka, Nami nemá únik.
support|Nami|Maokai|Vydrží její poke a engage vyhraje.
support|Nautilus|Taric|Stun a nesmrtelnost otočí jeho engage.
support|Nautilus|Braum|Štítem blokuje hook.
support|Nautilus|Leona|Vydrží jeho engage a otočí ho vlastním.
support|Neeko|Soraka|Léčí a silence zastaví její engage.
support|Neeko|Thresh|Hookne ji a lantern zachrání spoluhráče.
support|Neeko|Janna|Disengage a poke, Neeko nemá jak engagovat.
support|Pyke|Rell|Vydrží jeho engage a otočí ho.
support|Pyke|Janna|Disengage a štíty mu kazí all-in.
support|Pyke|Maokai|Vydrží jeho burst a engage vyhraje.
support|Rakan|Leona|Vydrží jeho engage a otočí ho vlastním.
support|Rakan|Janna|Disengage mu kazí engage.
support|Rakan|Seraphine|Pokuje ho a stun ho zastaví.
support|Rell|Janna|Disengage jí kazí engage.
support|Rell|Taric|Stun a nesmrtelnost otočí její engage.
support|Rell|Renata Glasc|R otočí její engage proti jejímu týmu.
support|Renata Glasc|Leona|All-in zblízka, Renata nemá únik.
support|Renata Glasc|Lulu|Polymorph a štít jí kazí combo.
support|Renata Glasc|Nami|Léčí a bublina ji chytí.
support|Senna|Zilean|Bomby ji pokují a revive drží ADC naživu.
support|Senna|Shen|Taunt ji chytí a R pomůže týmu.
support|Seraphine|LeBlanc|Bursne ji a odskočí.
support|Seraphine|Elise|Cocoon ji chytí a burst ji zabije.
support|Sona|Blitzcrank|Hookne ji, Sona nemá únik.
support|Sona|Thresh|Hookne ji a lantern zachrání spoluhráče.
support|Sona|Alistar|All-in zblízka, Sona nemá únik.
support|Soraka|Karma|Pokuje ji a štít drží ADC.
support|Soraka|Rakan|Engagne na ni a Soraka nemá únik.
support|Soraka|Blitzcrank|Hookne ji, Soraka nemá únik.
support|Swain|Zyra|Rostliny a poke ho drží od lajny.
support|Swain|Lulu|Polymorph a štít mu kazí engage.
support|Swain|Vel'Koz|Má delší poke range.
support|Taric|Nami|Léčí a pokuje, Taric nemá jak engagovat.
support|Taric|Sona|Léčí a pokuje, Taric nemá jak engagovat.
support|Taric|Renata Glasc|R otočí jeho engage.
support|Vel'Koz|LeBlanc|Bursne ho a odskočí.
support|Vel'Koz|Blitzcrank|Hookne ho, Vel'Koz nemá únik.
support|Vel'Koz|Karma|Pokuje ho a štít drží ADC.
support|Yuumi|Alistar|All-in na ADC, Yuumi nic nezmůže.
support|Yuumi|Thresh|Hookne ADC a Yuumi nemá jak pomoct.
support|Yuumi|Nautilus|Hookne ADC a Yuumi nemá jak pomoct.
support|Zilean|Maokai|Vydrží jeho poke a engage vyhraje.
support|Zilean|Janna|Disengage a poke, Zilean nemá jak vyhrát trade.
support|Zyra|Zilean|Bomby ji pokují a revive drží ADC naživu.
support|Zyra|Nautilus|Hookne ji a engage vyhraje.
support|Zyra|Blitzcrank|Hookne ji, když stojí mimo rostliny.
"""

ALT_WHY = {}
for line in RAW.strip().splitlines():
    lane, enemy, alt, text = line.split("|", 3)
    ALT_WHY.setdefault(lane, {}).setdefault(enemy, {})[alt] = text
