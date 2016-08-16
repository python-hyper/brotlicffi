# -*- coding: utf-8 -*-
"""
test_compatibility
~~~~~~~~~~~~~~~~~~

Tests for names that exist purely for compatibility purposes.
"""
import brotli


def test_compatible_names():
    """
    Encoder modes are also defined as individual top-level names with the same
    names as in brotlimodule.cc from the library.
    """
    assert brotli.MODE_GENERIC is brotli.BrotliEncoderMode.GENERIC
    assert brotli.MODE_TEXT is brotli.BrotliEncoderMode.TEXT
    assert brotli.MODE_FONT is brotli.BrotliEncoderMode.FONT
