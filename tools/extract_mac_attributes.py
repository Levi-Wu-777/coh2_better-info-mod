"""只读导出 CoH2 SGA v7 属性；字典使用 Cope RGDTools 的 hash_dict.txt。"""

import argparse
import collections
import hashlib
import json
import struct
import zlib
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--hash-dictionary", type=Path, required=True)
    args = parser.parse_args()
    dictionary = read_dictionary(args.hash_dictionary)
    archive = args.archive.read_bytes()
    attributes, counts, unknown = read_archive(archive, dictionary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(attributes, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({
        "archive_sha256": hashlib.sha256(archive).hexdigest(),
        "counts": counts,
        "unknown_field_hashes": len(unknown),
        "output": str(args.output),
    }, ensure_ascii=False, indent=2))


def read_dictionary(path):
    names = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            names[int(key, 16)] = value
    return names


def read_archive(archive, dictionary):
    assert archive[:8] == b"_ARCHIVE"
    assert struct.unpack_from("<I", archive, 8)[0] == 7
    toc_base = 152
    data_base = struct.unpack_from("<I", archive, 144)[0]
    _, _, folders_base, folder_count, files_base, file_count, names_base, _ = struct.unpack_from("<8I", archive, toc_base)
    names_base += toc_base
    attributes = {}
    counts = collections.Counter()
    unknown = set()
    for folder_index in range(folder_count):
        name_offset, _, _, file_start, file_end = struct.unpack_from("<5I", archive, toc_base + folders_base + 20 * folder_index)
        folder_name = read_string(archive, names_base + name_offset)
        for file_index in range(file_start, file_end):
            name_offset, data_offset, stored_size, raw_size, _, verification, storage, crc, _ = struct.unpack_from("<5I2B2I", archive, toc_base + files_base + 30 * file_index)
            assert verification == 4
            assert storage in (0, 2)
            file_name = read_string(archive, names_base + name_offset)
            path = (folder_name + "\\" + file_name).replace("\\", "/")
            stored = archive[data_base + data_offset:data_base + data_offset + stored_size]
            assert zlib.crc32(stored) == crc, path
            raw = zlib.decompress(stored) if storage else stored
            assert len(raw) == raw_size, path
            assert path not in attributes, path
            if not raw:
                attributes[path] = {}
                counts["empty_type_definitions"] += 1
            elif path.endswith(".rgd"):
                assert raw[:12] == b"Relic Chunky", path
                assert raw[36:44] == b"DATAAEGD", path
                description_size = struct.unpack_from("<I", raw, 52)[0]
                attributes[path] = read_table(raw, 72 + description_size, dictionary, unknown)
                counts["decoded_rgd_files"] += 1
            else:
                counts["non_rgd_files"] += 1
    assert sum(counts.values()) == file_count
    return attributes, counts, unknown


def read_table(raw, position, dictionary, unknown):
    count = struct.unpack_from("<I", raw, position)[0]
    values_base = position + 4 + count * 12
    values = {}
    for index in range(count):
        key_hash, value_type, offset = struct.unpack_from("<3I", raw, position + 4 + index * 12)
        key = dictionary.get(key_hash, f"0x{key_hash:08x}")
        if key_hash not in dictionary:
            unknown.add(key_hash)
        value_position = values_base + offset
        if value_type in (100, 101):
            value = read_table(raw, value_position, dictionary, unknown)
        elif value_type == 0:
            value = struct.unpack_from("<f", raw, value_position)[0]
        elif value_type == 1:
            value = struct.unpack_from("<I", raw, value_position)[0]
        elif value_type == 2:
            value = bool(raw[value_position])
        elif value_type == 3:
            value = read_string(raw, value_position)
        elif value_type == 4:
            end = value_position
            while raw[end:end + 2] != b"\0\0":
                end += 2
            value = raw[value_position:end].decode("utf-16-le")
        else:
            raise ValueError(f"Unknown RGD type: {value_type}")
        suffix = 2
        unique_key = key
        while unique_key in values:
            unique_key = f"{key}#{suffix}"
            suffix += 1
        values[unique_key] = value
    return values


def read_string(raw, position):
    return raw[position:raw.index(0, position)].decode("utf-8")


if __name__ == "__main__":
    main()
