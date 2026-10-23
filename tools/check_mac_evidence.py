"""Check recorded Mac evidence against a fresh attribute export; this does not test engine behavior."""

import argparse
import collections
import hashlib
import json
import math
import mmap
import struct
import zlib
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attributes", type=Path)
    parser.add_argument("--game-root", type=Path, help="Steam game folder, for checking recorded SCAR and native executable evidence")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    attributes = json.loads(args.attributes.read_text(encoding="utf-8"))
    manifest = json.loads((root / "data/macos-1.3.8.json").read_text(encoding="utf-8"))
    checks = 0
    for correction in manifest["corrections"]:
        evidence = correction["evidence"]
        for item in evidence if isinstance(evidence, list) else [evidence]:
            if isinstance(item, dict) and "field" in item:
                actual = read_field(attributes[item["file"]], item["field"])
                assert matches_value(actual, item["value"]), (correction["id"], item)
                if "calculation" in item:
                    check_production_time(attributes, actual, item["calculation"])
                checks += 1
    audit_path = root / "data/macos-1.3.8-audit.json"
    if audit_path.exists():
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        check_audit_inventory(root, manifest, audit)
        for item in audit["attribute_evidence"]:
            actual = read_field(attributes[item["file"]], item["field"])
            digest = hashlib.sha256(json.dumps(actual, sort_keys=True).encode()).hexdigest()
            assert digest == item["value_sha256"], item
            if "calculation" in item:
                check_production_time(attributes, actual, item["calculation"])
            checks += 1
        if args.game_root:
            source_checks = check_source_evidence(args.game_root, audit)
            print(f"Verified {source_checks} recorded script and native executable sources.")
        else:
            print("Script and native executable sources were not checked; supply --game-root to include them.")
    print(f"Verified {checks} recorded attribute observations. Tooltip interpretation and runtime claims require separate review.")


def check_audit_inventory(root, manifest, audit):
    text = dict(line.split("\t", 1) for line in (root / "macos/RelicCoH2.English.ucs").read_bytes().decode("utf-16").splitlines())
    for entry in audit["entries"]:
        assert entry["text"] == text[entry["id"]], entry["id"]
        assert entry["text_sha256"] == hashlib.sha256(entry["text"].encode()).hexdigest(), entry["id"]
        for review in entry["reviews"]:
            assert all(0 <= index < len(audit["attribute_evidence"]) for index in review["evidence"]), entry["id"]
    counts = dict(collections.Counter(entry["status"] for entry in audit["entries"] if entry["in_numeric_inventory"]))
    assert counts == audit["results"]["numeric_inventory_status_counts"] == manifest["coverage"]["numeric_inventory_status_counts"]
    assert len(manifest["corrections"]) == audit["results"]["total_corrected_descriptions"]
    assert manifest["unresolved"]["ids"] == [entry["id"] for entry in audit["entries"] if entry["status"] == "needs_runtime"]


def check_source_evidence(game_root, audit):
    for item in audit["script_evidence"]:
        archive_path = game_root / "CompanyOfHeroes2Data/coh2/archives" / item["archive"]
        content = read_archive_file(archive_path, item["file"])
        check_file_evidence(content, item)
    for item in audit.get("native_evidence", []):
        content = (game_root / item["file"]).read_bytes()
        check_file_evidence(content, item)
    return len(audit["script_evidence"]) + len(audit.get("native_evidence", []))


def check_file_evidence(content, item):
    assert hashlib.sha256(content).hexdigest() == item["sha256"], item["file"]
    for segment in item.get("segments", []):
        offset = segment["offset"]
        expected = bytes.fromhex(segment["bytes_hex"])
        assert content[offset:offset + len(expected)] == expected, segment
    for excerpt in item.get("excerpts", []):
        lines = content.decode("utf-8-sig").splitlines()
        actual = "\n".join(lines[excerpt["start_line"] - 1:excerpt["end_line"]])
        assert actual == excerpt["text"], excerpt


def read_archive_file(path, requested_file):
    with path.open("rb") as archive_file, mmap.mmap(archive_file.fileno(), 0, access=mmap.ACCESS_READ) as archive:
        assert archive[:8] == b"_ARCHIVE" and struct.unpack_from("<I", archive, 8)[0] == 7
        toc_base = 152
        data_base = struct.unpack_from("<I", archive, 144)[0]
        _, _, folders_base, folder_count, files_base, _, names_base, _ = struct.unpack_from("<8I", archive, toc_base)
        names_base += toc_base
        for folder_index in range(folder_count):
            name_offset, _, _, start, end = struct.unpack_from("<5I", archive, toc_base + folders_base + 20 * folder_index)
            folder = read_archive_string(archive, names_base + name_offset)
            for file_index in range(start, end):
                name_offset, data_offset, stored_size, raw_size, _, verification, storage, crc, _ = struct.unpack_from("<5I2B2I", archive, toc_base + files_base + 30 * file_index)
                name = read_archive_string(archive, names_base + name_offset)
                if (folder + "/" + name).replace("\\", "/").lstrip("/") != requested_file:
                    continue
                assert verification == 4 and storage in (0, 2)
                stored = archive[data_base + data_offset:data_base + data_offset + stored_size]
                assert zlib.crc32(stored) == crc, requested_file
                content = zlib.decompress(stored) if storage else stored
                assert len(content) == raw_size, requested_file
                return content
    raise KeyError(requested_file)


def read_archive_string(archive, position):
    return archive[position:archive.find(b"\0", position)].decode("utf-8")


def read_field(value, field):
    keys = field.strip("/").split("/") if field.startswith("/") else field.split(".")
    for key in keys:
        value = value[key]
    return value


def matches_value(actual, expected):
    if isinstance(actual, dict) and isinstance(expected, dict):
        return actual.keys() >= expected.keys() and all(matches_value(actual[key], expected[key]) for key in expected)
    if isinstance(actual, list) and isinstance(expected, list):
        return len(actual) == len(expected) and all(matches_value(a, b) for a, b in zip(actual, expected))
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        return math.isclose(actual, expected, rel_tol=1e-6, abs_tol=1e-6)
    return actual == expected


def check_production_time(attributes, loadout, calculation):
    total = 0
    for entity in calculation["entities"]:
        members = [member for member in loadout.values() if member["type"] == Path(entity["file"]).stem]
        assert len(members) == 1 and members[0]["num"] == entity["count"], entity
        timer = read_field(attributes[entity["file"]], "cost_ext.time_cost.time_seconds")
        assert matches_value(timer, entity["time_seconds"]), entity
        total += members[0]["num"] * timer
    assert matches_value(total, calculation["sum_count_times_entity_cost_time"]), calculation


if __name__ == "__main__":
    main()
