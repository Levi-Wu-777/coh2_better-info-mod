"""Check derived sight descriptions against recorded attribute evidence."""

import json
import re
import unittest
from pathlib import Path


def read_evidence(correction, suffix):
    matches = [
        item["value"] for item in correction["evidence"]
        if isinstance(item, dict) and item["field"].endswith(suffix)
    ]
    assert len(matches) == 1, suffix
    return matches[0]


class SightDescriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / "data/macos-1.3.8.json").read_text(encoding="utf-8"))
        cls.corrections = {item["id"]: item for item in manifest["corrections"]}
        localization = (root / "macos/RelicCoH2.English.ucs").read_bytes().decode("utf-16")
        cls.strings = dict(line.split("\t", 1) for line in localization.splitlines())

    def test_sniper_sight_matches_base_and_veterancy_multiplier(self):
        for identifier in ["11009062", "11009065", "11083378"]:
            with self.subTest(identifier=identifier):
                correction = self.corrections[identifier]
                base = read_evidence(correction, "sight_ext.sight_package.outer_radius")
                modifier = read_evidence(correction, "sight_radius_modifier")
                self.assertEqual(modifier["usage_type"], "multiplication")
                match = re.search(r"Sight: ([\d.]+),([\d.]+) \(at Vet2\)", self.strings[identifier])
                self.assertIsNotNone(match)
                assert match is not None
                self.assertAlmostEqual(float(match[1]), base)
                self.assertAlmostEqual(float(match[2]), base * modifier["value"])

    def test_pyrotechnics_sight_matches_upgrade_description(self):
        correction = self.corrections["11083367"]
        base = read_evidence(correction, "sight_ext.sight_package.outer_radius")
        modifier = read_evidence(correction, "sight_radius_modifier")
        self.assertEqual(modifier["usage_type"], "addition")
        match = re.search(r"Sight: ([\d.]+),([\d.]+) \[with 'Pyrotechnics Supplies' Upgrade\]", self.strings["11083367"])
        self.assertIsNotNone(match)
        assert match is not None
        self.assertAlmostEqual(float(match[1]), base)
        self.assertAlmostEqual(float(match[2]), base + modifier["value"])
        upgrade_match = re.search(r"\+ ([\d.]+) sight", self.strings["11090777"])
        self.assertIsNotNone(upgrade_match)
        assert upgrade_match is not None
        self.assertAlmostEqual(float(upgrade_match[1]), modifier["value"])


if __name__ == "__main__":
    unittest.main()
