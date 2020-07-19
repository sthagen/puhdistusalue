# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pathlib
import pytest  # type: ignore

import purge_range.cli as cli


def test_main_nok_empty():
    assert cli.main([]) is None


def test_main_nok_int():
    message = r"argument of type 'int' is not iterable"
    with pytest.raises(TypeError, match=message):
        cli.main(42)


def test_main_nok_ints():
    sequence_of_ints = [1, 2, 3]
    assert pathlib.Path(str(sequence_of_ints[0])).is_dir() is False, "Unexpected folder 1 exists which breaks this test"
    message = f"\\[Errno 20\\] Not a directory: {sequence_of_ints[0]}"
    with pytest.raises(NotADirectoryError, match=message):
        cli.main(sequence_of_ints)
