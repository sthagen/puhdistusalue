# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pytest  # type: ignore

import purge_range.cli as cli


def test_main_nok_empty():
    assert cli.main([]) is None
