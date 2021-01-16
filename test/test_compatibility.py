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
        brotli_version = int(
            re.search(
                r"#define BROTLI_VERSION 0x([A-Fa-f0-9]+)", f.read()
            ).group(1),
            16,
        )
        major = brotli_version >> 24
        minor = (brotli_version >> 12) & 0xFFF
        patch = brotli_version & 0xFFF
        assert brotlicffi.__version__.startswith(
            "%d.%d.%d." % (major, minor, patch)
        )
