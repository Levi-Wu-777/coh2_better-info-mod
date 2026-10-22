"""Check recorded Mac evidence against a fresh attribute export; this does not test engine behavior."""

import argparse
import hashlib
import json
import math
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attributes", type=Path)
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
        for item in audit["attribute_evidence"]:
            actual = read_field(attributes[item["file"]], item["field"])
            digest = hashlib.sha256(json.dumps(actual, sort_keys=True).encode()).hexdigest()
            assert digest == item["value_sha256"], item
            if "calculation" in item:
                check_production_time(attributes, actual, item["calculation"])
            checks += 1
    print(f"Verified {checks} recorded attribute observations. Tooltip interpretation and runtime claims require separate review.")


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
