#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Purge monotonically named files in folders keeping range endpoints.

Implementation uses sha256 hashes for identity and assumes that
the natural order relates to the notion of fresher or better.
"""
import os
import sys
import typing

from puristaa.puristaa import prefix_compression  # type: ignore

from puhdistusalue.puhdistusalue import read_folder, triage_hashes

DEBUG = os.getenv('PURGE_RANGE_DEBUG')


# pylint: disable=expression-not-assigned
@typing.no_type_check
def main(argv=None):
    """Process the files separately per folder."""
    argv = sys.argv[1:] if argv is None else argv
    verbose = True if '-v' in argv or '--verbose' in argv else False
    folder_paths = [entry for entry in argv if entry not in ('-v', '--verbose')]
    total_removed, total_less_bytes = 0, 0
    for a_path in folder_paths:
        hash_map = read_folder(a_path)
        keep_these, remove_those = triage_hashes(hash_map)
        for this in keep_these:
            DEBUG and print(f'KEEP file {this}')
        folder_removed, folder_less_bytes = 0, 0
        for that in remove_those:
            DEBUG and print(f'REMOVE file {that}')
            target = os.path.join(a_path, that)
            folder_less_bytes += os.path.getsize(target)
            os.remove(target)
            folder_removed += 1

        if verbose:
            print(
                f'removed {folder_removed} redundant objects or {folder_less_bytes}'
                f' combined bytes from folder at {a_path}'
            )
        total_less_bytes += folder_less_bytes
        total_removed += folder_removed

    prefix, rel_paths = prefix_compression(folder_paths, policy=lambda x: x == '/')
    if len(rel_paths) > 5:
        folders_disp = f"{prefix}[{', '.join(rel_paths[:3])}, ... {rel_paths[-1]}]"
    else:
        folders_disp = f'{folder_paths}'
    print(
        f'removed {total_removed} total redundant objects or {total_less_bytes}'
        f' total bytes from folders at {folders_disp}'
    )
