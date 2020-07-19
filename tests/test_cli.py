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
    nef = str(sequence_of_ints[0])
    assert pathlib.Path(nef).is_dir() is False, f"Unexpected folder {nef} exists which breaks this test"
    message = f"\\[Errno 20\\] Not a directory: {sequence_of_ints[0]}"
    with pytest.raises(NotADirectoryError, match=message):
        cli.main(sequence_of_ints)


def test_main_nok_non_existing_folder():
    nef = non_existing_folder_path = 'folder_does_not_exist'
    assert pathlib.Path(nef).is_dir() is False, f"Unexpected folder {nef} exists which breaks this test"
    message = f"\\[Errno 2\\] No such file or directory: '{non_existing_folder_path}'"
    with pytest.raises(FileNotFoundError, match=message):
        cli.main([non_existing_folder_path])
