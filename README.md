# Company of Heroes 2 - Better-Info-Mod

Project
------

> The "mod" is basically just a rewritten text file. Each text entry in the game has a unique key ID in that text file, and the associated text has been edited to be actually useful.
> 
> Company of Heroes 2 is a game full of units, abilities and mechanics. However, the UI's explanation of these is often vague or outdated. This leads to the fact that hardly anyone looks at the descriptions more than once, and those who want to know more details has to do research outside the game with sources that are often outdated themselves.
> 
> The mod takes descriptions of abilities, veterancy changes, units, build time, upgrades, aura buffs, damage dealt, etc. and replaces them with the most accurate, comprehensible values possible.
> 
> Now you will get accurate and actually helpful information by hovering your mouse over the respective icon, veteran star or unit descriptions in the lower part of the screen.
> 
> Here are some examples:
> 
> ![Better-Info-Mod Image 01](https://www.coh2.org/file/20468/coh2-betterinfmod-02.png)
> 
> ![Better-Info-Mod Image 02](https://www.coh2.org/file/20469/coh2-betterinfmod-03.png)
> 
> ![Better-Info-Mod Image 03](https://www.coh2.org/file/20470/coh2-betterinfmod-04.png)
> 
> ![Better-Info-Mod Image 04](https://www.coh2.org/file/20471/coh2-betterinfmod-05.png)
> 
> **What are the modification?**
> 
> - Shows more detailed unit veterancy descriptions (i.e. an up-to-date *Numerical Veterancy Description Mod* - See section below).
> - For vehicles, shows armor values, health points and weapon range (if beyond default). Also shows damage and penetration (near-far) values for tanks.
> - For team weapons, shows penetration and range. Also shows damage and Penetration for artillery, mortars and anti-tank guns.
> - Additional detailed descriptions for most skills, commander abilities, upgrades and aura buffs (small portrait icons).
> - Shows the sight range of infantry and light vehicles (if beyond default 35m Range).
> - Shows the repair rates of engineers and and their upgrades (minesweepers, etc.).
> - Shows explosive damage of mines, snares and anti-tank weapons. It also shows the penetration of anti-tank weapons used by infantry.
> - Shows the (de)capture rate (if higher than 1.0) for infantry and light vehicles.
> - Shows build times for tech upgrades and base buildings.

[Source](https://www.coh2.org/news/110870/better-info-mod)

**Numerical Veterancy Description Mod**

> Have you ever wanted to know the numerical veterancy bonuses in game, without going to the [COH2.ORG guide](https://www.coh2.org/guides/29892/the-company-of-heroes-2-veterancy-guide)? Yeah! It's great that my rifleman receives `...more experience from extensive combat, increasing weapon lethality, increased durability, reducing ability recharge, and increasing ability range`, but how much exactly? I am glad that my riflemen got so much out of their extensive combat, but I WANT NUMBERS.
>
> Now you can get exact numbers in game with this great mod. It works in automatch too! With this mod, no more colourful and vague descriptions - only straight talk!
>
> ![Numerical Veterancy Description Image](https://www.coh2.org/file/13006/veterancy.jpg)

[Source](https://www.coh2.org/news/58454/numerical-veterancy-description)

Feedback? Contribution?
-----------

If you find a typo/error, see information missing, have other suggestions, or want to help to translate the mod for another language, please don't hesitate to contact us. You can reach out in two ways:

- [CoHmmunity Germany Discord](https://discord.gg/zUJRw8juFk);
- [Github](https://github.com/Mithiriath/coh2_better-info-mod/issues);

Notation
-----------

- Armor: `<front>;<rear>`
- Damage: `<penetration damage>`(`<deflection damage if exist>`)
- Duration: `<duration of the ability>`
- HP: `<hp>`
- Penetration: `<same value at all range>`
- Penetration: `<short>,<medium>,<long>` range
- Penetration near-far: `<near>-<far>`
- Range: `<max firing range>`
- Range of aura: `<max aura range>`
- Sight: `<range if different than the default 35 range>`
- *: Means that the statistic of the unit increases when the unit gains veterancy.

Authors
-----------

### Better-Info-Mod

Thanks to jamesjamozo for the English and the German version.

Thanks to Osinyagov for the Russian translation.

### Numerical Veterancy Description Mod

Thanks to Sarantini for making the [Veterancy Guide](https://www.coh2.org/guides/29892/the-company-of-heroes-2-veterancy-guide) in early 2015 and CookiezNcreem and Tobis for updating it.

Thanks to Harold for being the first to come up with the [Numerical Veterancy Description Mod](https://www.coh2.org/topic/58241/numeral-veterancy-descriptions-english-localization-mod) in 2015.

Thanks to Osinyagov and RussianHamster (aka XaMiaK) for the [Russian version](https://www.coh2.org/topic/60155/numeral-veterancy-descriptions-russian-localization-mod).

Thanks to jamesjamozo and Karotten Harry for updating the English version and for the translation for the German version.

Thanks to 3nder990 for the translation for the Spanish version.

Download
-----------

You can dowload the mod [from github](https://github.com/Mithiriath/coh2_better-info-mod/releases).

Click on the link above, *Assets* section, then click on *Source code (zip)*.

[![Github Download Mod Procedure Image](https://www.coh2.org/file/20453/github-download-mod-procedure.png)](https://github.com/Mithiriath/coh2_better-info-mod/releases)

Installation
-----------

* If CoH 2 is started, stop the game;
* Go to your Steam Library and right-click CoH 2;
* Click on *Properties...* -> *Local Files* -> *Browse...* to open your CoH 2 directory;
* Go to the folder: *CoH2* -> *Locale* -> *English* (if you have your game in English. Czech/French/German/Italian/Polish/Russian/Spanish folder if you have your game in an other language);
* Replace the file *RelicCoH2.English.ucs* (if you have your game in English) by the new file you downloaded;
* If you have your game in Czech for example and want to use the *RelicCoH2.English.ucs* file from the mod, you can. You just copy *RelicCoH2.English.ucs* file in your *Czech* folder then rename it *RelicCoH2.Czech.ucs*.

If you want to restore the file:
* If CoH 2 is started, stop the game;
* Go to your Steam Library and right-click CoH 2;
* Click on *Properties...* -> *Local Files* -> *Verify integrity of game files...*;

## macOS 1.3.8 correction pack

This fork adds an English correction pack for the native Feral Mac port, version 1.3.8 (build 306362.56045), using local game attributes as evidence. It corrects 564 descriptions without changing gameplay attributes.

### Mac installation

Use [macos/RelicCoH2.English.ucs](macos/RelicCoH2.English.ucs) for this correction pack. Quit the game, browse its local files in Steam, and open `CompanyOfHeroes2Data/coh2/locale/english/`. Back up `reliccoh2.english.ucs`, then replace it with the corrected file, keeping the destination filename.

The pack targets standard multiplayer rules. Campaigns, Theater of War, balance mods, Windows/Wine installations, and other languages are outside the reviewed scope. Individual changes have not been tested in-game.

### Correction data and tools

- [data/macos-1.3.8.json](data/macos-1.3.8.json) records original and corrected text, attribute evidence, version hashes, and unresolved cases.
- [data/macos-1.3.8-audit.json](data/macos-1.3.8-audit.json) records the complete numerical audit inventory: 1,191 modified numerical texts plus 366 baseline candidates, per-component findings, source references, and runtime limits. The `followup` section groups the original 150 pending IDs; each entry retains its specific remaining question. `current_text_status` describes the revised wording separately from unresolved mechanics. Entries marked `needs_runtime` are not fully verified, even if a supported part was corrected or an unsupported number removed.
- [tools/check_mac_evidence.py](tools/check_mac_evidence.py) checks recorded fields, production-time arithmetic, audit text fingerprints, and optional SCAR/native executable source fingerprints. Source-byte matches do not certify the interpretation of engine behavior.
- [tools/build_macos.py](tools/build_macos.py) generates the Mac file and verifies it against the correction manifest.
- [tools/extract_mac_attributes.py](tools/extract_mac_attributes.py) exports local SGA v7 attributes without modifying the archive; it verifies CRCs and decompressed lengths and preserves unknown fields and repeated entries.
- [tests/test_build_macos.py](tests/test_build_macos.py) checks localization integrity.

The root-level English and German files match the official v1.2 release attachment. Other upstream localization files are retained. Repository documentation, code comments, tool messages, and correction notes use English.

Requires Python 3 with no additional Python dependencies:

```sh
python3 tools/build_macos.py
python3 tools/build_macos.py --check
python3 -m unittest discover -s tests
```

To extract attributes, obtain `hash_dict.txt` from the [RGDTools archive used by CoH2 Stats](https://raw.githubusercontent.com/cohstats/coh2stats/master/scripts/RGDTools_v1.3.7z), then run:

```sh
python3 tools/extract_mac_attributes.py /path/to/attribarchive.sga /tmp/attributes.json --hash-dictionary /path/to/hash_dict.txt
```

Do not commit complete game attribute exports or third-party dictionaries. The Mac version scope follows [Feral's official patch information](https://steamcommunity.com/app/231430/discussions/0/3040481757531253611/).

To check the recorded evidence against the extracted attributes:

```sh
python3 tools/check_mac_evidence.py /tmp/attributes.json --game-root "/path/to/Company of Heroes 2"
```

The optional game folder checks recorded SCAR file hashes/excerpts and native x86_64 executable hashes/instruction bytes directly from the local installation. Complete game scripts, binaries, and disassembler dependencies are not included. These are static source observations; no in-game verification is implied.
