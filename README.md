# Better Info Mod · macOS 1.3.8

English tooltip corrections for the Feral Mac version of Company of Heroes 2, version 1.3.8 (build 306362.56045). The current release corrects 180 descriptions and changes displayed text only, leaving gameplay attributes unchanged.

Repository documentation, code comments, tool messages, and correction notes use English.

## Files

- `macos/RelicCoH2.English.ucs`: the installable English localization for Mac.
- `data/macos-1.3.8.json`: original and corrected text, local attribute evidence, version information, hashes, and unresolved cases.
- `tools/`: localization generation, verification, and SGA v7 attribute extraction tools.
- `tests/`: localization integrity tests.
- Root-level `.ucs` files: upstream localization files. English and German match the official v1.2 release archive. Other languages retain their upstream versions and have not been corrected for Mac.
- `src/`: original localization files retained from upstream.

## Installation

Quit the game. In Steam, browse the local files for Company of Heroes 2 and open `CompanyOfHeroes2Data/coh2/locale/english/`. Back up the existing `reliccoh2.english.ucs`, then replace it with this repository's `macos/RelicCoH2.English.ucs`, keeping the destination filename.

This version targets the native Mac port and standard multiplayer rules. Campaigns, Theater of War, balance mods, Windows/Wine installations, and other languages are outside the reviewed scope. See the correction manifest for unresolved cases. Individual changes have not been tested in-game.

## Build and verify

Requires Python 3 with no additional Python dependencies.

```sh
python3 tools/build_macos.py
python3 tools/build_macos.py --check
python3 -m unittest discover -s tests
```

To extract local attributes again, obtain `hash_dict.txt` from the [RGDTools archive used by CoH2 Stats](https://raw.githubusercontent.com/cohstats/coh2stats/master/scripts/RGDTools_v1.3.7z), then run:

```sh
python3 tools/extract_mac_attributes.py /path/to/attribarchive.sga /tmp/attributes.json --hash-dictionary /path/to/hash_dict.txt
```

The extraction tool reads the SGA without modifying it, verifies stored-data CRCs and decompressed lengths, and preserves unknown fields and repeated array entries. Do not commit complete game attribute exports or third-party dictionaries to this repository.

## Sources and credits

Based on [Mithiriath/coh2_better-info-mod](https://github.com/Mithiriath/coh2_better-info-mod) and its [official v1.2 release archive](https://github.com/Mithiriath/coh2_better-info-mod/releases/tag/v1.2). Thanks to Mithiriath, jamesjamozo, Elpern, Osinyagov, and the original Numerical Veterancy Description Mod contributors: Sarantini, CookiezNcreem, Tobis, Harold, RussianHamster, Karotten Harry, and 3nder990.

The version scope follows [Feral's official Mac patch information](https://steamcommunity.com/app/231430/discussions/0/3040481757531253611/). Corrected values are based on this version's local `attribarchive.sga`.
