"""检查本地化生成过程中 ID、编码和未修改文字的完整性。"""

import copy
import hashlib
import runpy
import unittest
from pathlib import Path


build_localization = runpy.run_path(
    str(Path(__file__).resolve().parents[1] / "tools/build_macos.py")
)["build_localization"]


class LocalizationTests(unittest.TestCase):
    def setUp(self):
        self.source = "1\tOriginal\\nLine\r\n2\t保留原文\r\n".encode("utf-16")
        self.manifest = {
            "source": {"english_sha256": hashlib.sha256(self.source).hexdigest()},
            "corrections": [{
                "id": "1",
                "before": "Original\\nLine",
                "after": "Corrected\\nLine",
                "reason": "属性核对",
                "evidence": [{"file": "unit.rgd", "field": "armor", "value": 270}],
            }],
        }

    def test_preserves_ids_unicode_literal_newlines_and_crlf(self):
        output = build_localization(self.source, self.manifest)
        self.assertEqual(output, "1\tCorrected\\nLine\r\n2\t保留原文\r\n".encode("utf-16"))

    def test_rejects_changed_source(self):
        with self.assertRaises(AssertionError):
            build_localization(self.source + b"\0\0", self.manifest)

    def test_rejects_duplicate_or_missing_ids(self):
        duplicate = copy.deepcopy(self.manifest)
        duplicate["corrections"] *= 2
        missing = copy.deepcopy(self.manifest)
        missing["corrections"][0]["id"] = "3"
        for manifest in [duplicate, missing]:
            with self.subTest(manifest=manifest), self.assertRaises(AssertionError):
                build_localization(self.source, manifest)

    def test_rejects_stale_text_or_embedded_record_separators(self):
        for key, value in [("before", "Different"), ("after", "Broken\nRecord"), ("after", "Broken\tField")]:
            manifest = copy.deepcopy(self.manifest)
            manifest["corrections"][0][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(AssertionError):
                build_localization(self.source, manifest)


if __name__ == "__main__":
    unittest.main()
