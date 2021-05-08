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


def test_purge_range_ok_disjoint_strings():
    texts = ["a", "b"]
    assert pr.prefix_compression(texts) == ("", texts)


def test_purge_range_ok_empty():
    texts = []
    assert pr.prefix_compression(texts) == ("", texts)


def test_purge_range_nok_ints():
    message = r"'int' object is not iterable"
    with pytest.raises(TypeError, match=message):
        pr.prefix_compression([1, 2, 3])


def test_purge_range_nok_floats():
    message = r"'float' object is not iterable"
    with pytest.raises(TypeError, match=message):
        pr.prefix_compression([0.123, 3.1415])


def test_prefix_compression_documentation_ok_example():
    sequence = ["bar/baz", "bar/bazaar"]
    expect = ("bar/", ["baz", "bazaar"])
    assert pr.prefix_compression(sequence, policy=lambda x: x == "/") == expect


def test_prefix_compression_documentation_ok_no_policy_example():
    sequence = ["bar/baz", "bar/bazaar"]
    expect = ("bar/baz", ["", "aar"])
    assert pr.prefix_compression(sequence, policy=None) == expect


def test_prefix_compression_documentation_ok_tuple_no_policy_example():
    sequence = ("bar/baz", "bar/bazaar")
    expect = ("bar/baz", ["", "aar"])
    assert pr.prefix_compression(sequence, policy=None) == expect


def test_prefix_compression_documentation_nok_set_no_policy_example():
    sequence = {"bar/baz", "bar/bazaar"}
    message = r"'set' object is not subscriptable"
    with pytest.raises(TypeError, match=message):
        pr.prefix_compression(sequence, policy=None)


def test_prefix_compression_documentation_ok_dict_no_policy_example():
    mapping = {0: "bar/baz", 1: "bar/bazaar"}
    expect = ('', [{0: 'bar/baz', 1: 'bar/bazaar'}])
    assert pr.prefix_compression(mapping, policy=None) == expect


def test_prefix_compression_documentation_nok_class_instance_no_policy_example():
    class Foo:
        pass
    an_object = Foo()
    message = r"'Foo' object is not iterable"
    with pytest.raises(TypeError, match=message):
        pr.prefix_compression(an_object, policy=None)


def test_triage_hashes_ok_mixed_input():
    data = {
        "no": [("matter", 4), ("remove", 4), ("what", 4)],
        "we": [("keep", 1)],
        "maybe": [("empty", 0)],
    }
    keep, remove = pr.triage_hashes(data)
    assert keep == ['matter', 'what', 'keep']
    assert remove == ['remove', 'empty']


def test_triage_hashes_ok_mixed_input_no_reorder():
    data = {
        "a": [("z", 4), ("a", 4), ("y", 4)],
        "b": [("x", 1), ("y", 2), ("x", 3)],
        "c": [("_", 0)],
    }
    keep, remove = pr.triage_hashes(data)
    assert keep == ['z', 'y', 'x', 'x']
    assert remove == ['a', 'y', '_']
