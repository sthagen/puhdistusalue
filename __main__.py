#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Purge monotonically named files in folders keeping range endpoints.

Implementation uses sha256 hashes for identity and assumes that
the natural order relates to the notion of fresher or better.
"""
import hashlib
import os
import sys

BUFFER_BYTES = 2 << 15
DEBUG = os.getenv("PURGE_RANGE_DEBUG")


def list_dir(folder_path):
    """Access the dir and yield the local names inside."""
    return os.listdir(folder_path)


def elements_of_gen(folder_path):
    """Prefix names in folder path and yield sorted pairs of names and file paths."""
    for name in sorted(name for name in list_dir(folder_path)):
        yield name, os.path.join(folder_path, name)


def read_folder(folder_path, get_size=os.path.getsize):
    """Yield hash map of lists with name, byte size pairs of sorted by name (hint: timestamp)."""
    hash_map = {}
    for name, file_path in elements_of_gen(folder_path):
        with open(file_path, "rb") as in_file:
            sha256_hash = hashlib.sha256()
            for byte_block in iter(lambda in_f=in_file: in_f.read(BUFFER_BYTES), b""):
                sha256_hash.update(byte_block)
            hash_map.setdefault(sha256_hash.hexdigest(), []).append(
                (name, get_size(file_path))
            )
    return hash_map


def triage_hashes(hash_map):
    """Triage hash map in pair of names to keep and to remove in that order.

    Three cases:

    0. size zero regardless of hash => remove
    1. unique hash => keep
    2. hash matching two entries => keep both
    3. hash with more than two entries => keep first and last, rest remove
    """
    keep, remove = [], []
    for info in hash_map.values():
        if info[0][1] == 0:
            remove.extend(name for name, _ in info)
        else:
            if len(info) == 1:
                keep.extend(name for name, _ in info)
            else:
                first, last = info[0][0], info[-1][0]
                keep.extend([first, last])
                remove.extend(name for name, _ in info[1:-1])
    return keep, remove


# pylint: disable=expression-not-assigned
def main(argv=None):
    """Process the files separately per folder."""
    argv = sys.argv[1:] if argv is None else argv
    verbose = True if "-v" in argv or "--verbose" in argv else DEBUG
    folder_paths = [entry for entry in argv if entry not in ("-v", "--verbose")]
    total_removed, total_less_bytes = 0, 0
    for a_path in folder_paths:
        if a_path in ("-v", "--verbose"):
            continue
        hash_map = read_folder(a_path)
        keep_these, remove_those = triage_hashes(hash_map)
        for this in keep_these:
            verbose and print(f"KEEP file {this}")
        folder_removed, folder_less_bytes = 0, 0
        for that in remove_those:
            verbose and print(f"REMOVE file {that}")
            target = os.path.join(a_path, that)
            folder_less_bytes += os.path.getsize(target)
            os.remove(target)
            folder_removed += 1

        verbose and print(f"removed {folder_removed} redundant objects or {folder_less_bytes} combined bytes from folder at {a_path}")
        total_less_bytes += folder_less_bytes
        total_removed += folder_removed

    if len(folder_paths) > 5:
        folders_disp = f"[{', '.join(folder_paths[:3])}, ... {folder_paths[-1]}]"
    else:
        folders_disp = f"{folder_paths}"
    print(
        f"removed {total_removed} total redundant objects or {total_less_bytes} total bytes from folders at {folders_disp}"
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
