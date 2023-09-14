# -*- coding: utf-8 -*-
"""
test_compatibility
~~~~~~~~~~~~~~~~~~

Tests for names that exist purely for compatibility purposes.
"""
import re
from os.path import abspath, join, dirname
import brotlicffi


def test_compatible_names():
    """
    Encoder modes are also defined as individual top-level names with the same
    names as in brotlimodule.cc from the library.
    """
    assert brotlicffi.MODE_GENERIC is brotlicffi.BrotliEncoderMode.GENERIC
    assert brotlicffi.MODE_TEXT is brotlicffi.BrotliEncoderMode.TEXT
    assert brotlicffi.MODE_FONT is brotlicffi.BrotliEncoderMode.FONT


def test_brotli_version():
    """
    Test that the __version__ starts with the
    Brotli version that's compiled with.
    """
    version_h = join(
        dirname(dirname(abspath(__file__))), "libbrotli/c/common/version.h"
    )
    with open(version_h) as f:
        brotli_versions = dict(
            re.findall(
                r"#define BROTLI_VERSION_(MAJOR|MINOR|PATCH) ([0-9]+)",
                f.read()
            )
        )
        assert brotlicffi.__version__.startswith(
            "%s.%s.%s." % (
                brotli_versions["MAJOR"],
                brotli_versions["MINOR"],
                brotli_versions["PATCH"]
            )
        )
