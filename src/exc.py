# Picks for lane x champion pairs that have no matchup with 100+ games even in all ranks over 30 days.
# Chosen by the enemy's class; the win rate shown is the pick's overall Emerald+ win rate in that lane.
EXC = {
    ("top", "enchanter"): [
        ("Sett", "Enchanter na topu nemá damage a Settův all-in s W ho rozdrtí."),
        ("Darius", "Enchanter nemá únik a pull s bleedem ho v lajně rozloží."),
        ("Pantheon", "Je silný early a stun z W chytí enchantera dřív, než se vyléčí."),
    ],
    ("top", "catcher"): [
        ("Garen", "Engage support na topu nemá damage a Garen ho v dlouhém tradu přetlačí."),
        ("Mordekaiser", "R ho odřízne od pomoci a magic damage ho rozloží."),
        ("Darius", "Engage support nemá damage na trade a Darius ho pullem a bleedem v lajně trestá."),
    ],
    ("jungle", "mage"): [
        ("Briar", "Mage v jungli clearuje pomalu a Briar ho early invaduje a zabije u kempů."),
        ("Rek'Sai", "Invaduje ho early a tunely jí dávají ganky dřív, než se mage rozjede."),
        ("Kha'Zix", "Mage v jungli bývá sám a Kha'Zix ho přes pasiv izolace bursne."),
    ],
    ("jungle", "adc"): [
        ("Rek'Sai", "Invaduje ho early a knockup ho chytí, ADC v jungli nemá únik."),
        ("Xin Zhao", "ADC v jungli se nemá jak bránit a Xin ho skokem z E dostihne."),
        ("Kha'Zix", "ADC v jungli bývá sám a Kha'Zix ho přes pasiv izolace bursne."),
    ],
    ("jungle", "enchanter"): [
        ("Briar", "Enchanter v jungli clearuje pomalu a Briar ho early invaduje."),
        ("Rek'Sai", "Invaduje ho early a tunely jí dávají ganky, enchanter v jungli nestíhá."),
        ("Kha'Zix", "Enchanter nemá damage a Kha'Zix ho bursne, když je sám."),
    ],
    ("jungle", "catcher"): [
        ("Shaco", "Engage support v jungli clearuje pomalu a Shaco ho early invaduje."),
        ("Xin Zhao", "Engage support v jungli nemá damage a Xin ho v souboji rozseká."),
        ("Viego", "Vyhraje duel a resety mu dávají skirmishe, engage support v jungli nemá damage."),
    ],
    ("jungle", "assassin"): [
        ("Rammus", "Armor z W tlumí burst assassina a taunt ho chytí."),
        ("Sejuani", "Vydrží burst assassina a CC ho zastaví."),
        ("Jarvan IV", "Je silný early a engage s CC assassina zastaví."),
    ],
    ("jungle", "specialist"): [
        ("Briar", "Off-meta jungler clearuje pomalu a Briar ho early invaduje."),
        ("Rek'Sai", "Invaduje ho early a tunely jí dávají rychlé ganky."),
        ("Viego", "Vyhraje duel a resety mu dávají skirmishe."),
    ],
    ("mid", "enchanter"): [
        ("Talon", "Enchanter na midu nemá damage a Talon ho bursne a roamuje."),
        ("LeBlanc", "Bursne enchantera dřív, než se stihne štítnout, a odskočí přes W."),
        ("Zed", "Je mobilnější a enchantera bursne přes stín."),
    ],
    ("mid", "catcher"): [
        ("Vladimir", "Bazén mu uhne z engage a v lajně supporta přefarmí."),
        ("Lissandra", "Engage support na midu nemá damage a Lissandra ho zmrazí a pokuje."),
        ("Malzahar", "Pasivní štít pohltí jeho engage a R ho chytí."),
    ],
    ("mid", "assassin"): [
        ("Lissandra", "Zmrazí assassina a R zastaví jeho all-in."),
        ("Malzahar", "Pasivní štít pohltí jeho burst a R ho chytí."),
        ("Galio", "Vydrží burst assassina a W ho tauntne."),
    ],
    ("mid", "bruiser"): [
        ("Vladimir", "Bazén mu uhne z all-inu a léčení ho drží v lajně."),
        ("Malzahar", "Pasivní štít pohltí jeho trade a R ho chytí."),
        ("Anivia", "Zeď ho odřízne a z dálky ho kituje."),
    ],
    ("bottom", "enchanter"): [
        ("Samira", "Enchanter na botu nemá damage a Samira ho v all-inu rozseká."),
        ("Draven", "Je silný early a sekyry enchantera v lajně zničí."),
        ("Lucian", "Krátké trady s dashem enchantera trestají a ten nemá jak odpovědět."),
    ],
    ("bottom", "tank"): [
        ("Kog'Maw", "Má dlouhý range a % HP damage tanka rozloží."),
        ("Vayne", "W s true damagem tanka rozloží a condemn ho odhodí."),
        ("Aphelios", "Kituje tanka z range a v teamfightu ho přeroste."),
    ],
    ("bottom", "bruiser"): [
        ("Jinx", "Kituje bruisera z range a E chompers ho chytí."),
        ("Ashe", "Slow z autoattacků bruisera kituje a R ho stunne."),
        ("Caitlyn", "Má dlouhý range a pasti bruisera zastaví."),
    ],
    ("bottom", "assassin"): [
        ("Jinx", "Kituje assassina z range a E chompers ho chytí."),
        ("Sivir", "Štít zablokuje burst assassina a v lajně ho přefarmí."),
        ("Ashe", "Slow assassina kituje a R ho stunne."),
    ],
    ("bottom", "catcher"): [
        ("Jinx", "Má dlouhý range a engage supportu potrestá chompers z E."),
        ("Sivir", "Štít zablokuje jeho engage a vlnu čistí rychleji."),
        ("Caitlyn", "Má dlouhý range a pasti jeho engage zastaví."),
    ],
    ("bottom", "mage"): [
        ("Samira", "Zblízka mage rozseká a W zablokuje jeho projektily."),
        ("Draven", "Je silný early a sekyry mage v lajně zničí."),
        ("Lucian", "Dashem uhne skillshotům a v krátkých tradech mage přebije."),
    ],
    ("bottom", "specialist"): [
        ("Caitlyn", "Má nejdelší range na botu a off-meta pick trestá autoattacky i pastmi."),
        ("Jinx", "Kituje z range a v late game off-meta pick přeroste."),
        ("Ashe", "Slow z autoattacků drží off-meta pick od těla a R ho stunne."),
    ],
    ("support", "adc"): [
        ("Leona", "ADC na supportu nemá CC ani odolnost a Leona ho engagne kdykoli."),
        ("Blitzcrank", "Hookne ADC, který se nemá jak bránit."),
        ("Nautilus", "Hookne ho a CC ho drží, ADC na supportu nevydrží."),
    ],
    ("support", "bruiser"): [
        ("Braum", "Štít zastaví jeho engage a pasiv ho stunne."),
        ("Janna", "Disengage mu kazí engage."),
        ("Zyra", "Rostliny ho trestají a root ho chytí."),
    ],
}
