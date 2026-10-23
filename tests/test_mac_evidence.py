"""Reject stale script excerpts and native instruction evidence."""

import copy
import hashlib
import runpy
import unittest
from pathlib import Path


check_file_evidence = runpy.run_path(
    str(Path(__file__).resolve().parents[1] / "tools/check_mac_evidence.py")
)["check_file_evidence"]


class SourceEvidenceTests(unittest.TestCase):
    def test_rejects_changed_script_or_wrong_line_range(self):
        content = b"function Start()\n    return 4\nend\n"
        record = {
            "file": "test.scar",
            "sha256": hashlib.sha256(content).hexdigest(),
            "excerpts": [{"start_line": 2, "end_line": 2, "text": "    return 4"}],
        }
        check_file_evidence(content, record)
        with self.assertRaises(AssertionError):
            check_file_evidence(content.replace(b"4", b"5"), record)
        wrong_range = copy.deepcopy(record)
        wrong_range["excerpts"][0]["start_line"] = 1
        with self.assertRaises(AssertionError):
            check_file_evidence(content, wrong_range)

    def test_rejects_instruction_bytes_at_wrong_offset(self):
        content = bytes.fromhex("9090f30f59059090")
        record = {
            "file": "test-executable",
            "sha256": hashlib.sha256(content).hexdigest(),
            "segments": [{"offset": 2, "bytes_hex": "f30f5905"}],
        }
        check_file_evidence(content, record)
        record["segments"][0]["offset"] = 3
        with self.assertRaises(AssertionError):
            check_file_evidence(content, record)


if __name__ == "__main__":
    unittest.main()
