# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pytest  # type: ignore

import purge_range.purge_range as pr


def test_triage_hashes_ok_empty_hash_map():
    assert pr.triage_hashes({}) == ([], [])


def test_prefix_compression_ok_string():
    texts = "imension is implicit"
    assert pr.prefix_compression(texts) == (texts, [""])


def test_purge_range_ok_same_chars_in_string():
    texts = "a a a a"
    assert pr.prefix_compression(texts) == (texts, [""])


def test_purge_range_ok_sequence_string():
    assert pr.prefix_compression(["aa"]) == ("aa", [""])


def test_purge_range_ok_strings():
    assert pr.prefix_compression(["aa", "ab"]) == ("a", ["a", "b"])
