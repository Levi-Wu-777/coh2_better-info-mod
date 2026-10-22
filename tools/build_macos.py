"""生成或验证 Mac 1.3.8 英文说明文件，不修改游戏安装目录。"""

import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="核对已生成文件")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "data/macos-1.3.8.json").read_text(encoding="utf-8"))
    source = (root / "RelicCoH2.English.ucs").read_bytes()
    output = build_localization(source, manifest)
    destination = root / "macos/RelicCoH2.English.ucs"
    if args.check:
        assert destination.read_bytes() == output, "Mac 文件与校正清单不一致"
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(output)
    print(f"已{'验证' if args.check else '生成'} {len(manifest['corrections'])} 条校正：{destination}")


def build_localization(source, manifest):
    assert hashlib.sha256(source).hexdigest() == manifest["source"]["english_sha256"]
    assert source[:2] == b"\xff\xfe", "源文件必须使用 UTF-16 LE BOM"
    lines = source.decode("utf-16").splitlines(keepends=True)
    corrections = {str(item["id"]): item for item in manifest["corrections"]}
    assert len(corrections) == len(manifest["corrections"]), "校正清单中存在重复 ID"
    seen = set()
    applied = set()
    output = []
    for line in lines:
        assert line.endswith("\r\n"), "源文件行尾格式不一致"
        identifier, text = line[:-2].split("\t", 1)
        assert identifier.isdecimal() and identifier not in seen, identifier
        seen.add(identifier)
        if identifier in corrections:
            item = corrections[identifier]
            assert text == item["before"], f"源文字发生变化：{identifier}"
            assert item["after"] != text and item["reason"] and item["evidence"], identifier
            assert not any(character in item["after"] for character in "\t\r\n"), identifier
            text = item["after"]
            applied.add(identifier)
        output.append(f"{identifier}\t{text}\r\n")
    assert applied == set(corrections), "校正清单包含不存在的 ID"
    return b"\xff\xfe" + "".join(output).encode("utf-16-le")


if __name__ == "__main__":
    main()
