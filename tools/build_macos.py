"""Build or verify the Mac 1.3.8 English localization without changing the game installation."""

import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify the generated file")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "data/macos-1.3.8.json").read_text(encoding="utf-8"))
    source = (root / "RelicCoH2.English.ucs").read_bytes()
    output = build_localization(source, manifest)
    destination = root / "macos/RelicCoH2.English.ucs"
    if args.check:
        assert destination.read_bytes() == output, "Mac localization does not match the correction manifest"
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(output)
    action = "Verified" if args.check else "Built"
    print(f"{action} {len(manifest['corrections'])} corrections: {destination}")


def build_localization(source, manifest):
    assert hashlib.sha256(source).hexdigest() == manifest["source"]["english_sha256"]
    assert source[:2] == b"\xff\xfe", "Source must use a UTF-16 LE BOM"
    lines = source.decode("utf-16").splitlines(keepends=True)
    corrections = {str(item["id"]): item for item in manifest["corrections"]}
    assert len(corrections) == len(manifest["corrections"]), "Duplicate IDs in the correction manifest"
    seen = set()
    applied = set()
    output = []
    for line in lines:
        assert line.endswith("\r\n"), "Inconsistent source line endings"
        identifier, text = line[:-2].split("\t", 1)
        assert identifier.isdecimal() and identifier not in seen, identifier
        seen.add(identifier)
        if identifier in corrections:
            item = corrections[identifier]
            assert text == item["before"], f"Source text has changed: {identifier}"
            assert item["after"] != text and item["reason"] and item["evidence"], identifier
            assert not any(character in item["after"] for character in "\t\r\n"), identifier
            text = item["after"]
            applied.add(identifier)
        output.append(f"{identifier}\t{text}\r\n")
    assert applied == set(corrections), "The correction manifest references missing IDs"
    return b"\xff\xfe" + "".join(output).encode("utf-16-le")


if __name__ == "__main__":
    main()
