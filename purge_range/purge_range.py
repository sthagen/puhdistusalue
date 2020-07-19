#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Purge monotonically named files in folders keeping range endpoints.

Implementation uses sha256 hashes for identity and assumes that
the natural order relates to the notion of fresher or better.
"""
import hashlib
import os

BUFFER_BYTES = 2 << 15


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


def prefix_compression(texts, policy=None):
    """Return common prefix string abiding policy and compressed texts string list."""
    if not texts:  # Early out return empty prefix and empty sequence
        return "", texts
    if not isinstance(texts, (list, tuple)):
        texts = [texts]
    prefix_guard, first, last = 0, min(texts), max(texts)
    for pos, char in enumerate(first):
        if char == last[pos]:
            prefix_guard += 1
        else:
            break
    if policy:
        for here in range(prefix_guard - 1, -1, -1):
            if policy(first[here]):
                prefix_guard = here + 1
                break
    if not prefix_guard:  # Reduce memory pressure for all different texts
        return "", texts
    return first[:prefix_guard], [text[prefix_guard:] for text in texts]
