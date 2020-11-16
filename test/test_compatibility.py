# -*- coding: utf-8 -*-
"""
test_compatibility
~~~~~~~~~~~~~~~~~~

Tests for names that exist purely for compatibility purposes.
"""
import brotlicffi


def test_compatible_names():
    """
    Encoder modes are also defined as individual top-level names with the same
    names as in brotlimodule.cc from the library.
    """
    assert brotlicffi.MODE_GENERIC is brotlicffi.BrotliEncoderMode.GENERIC
    assert brotlicffi.MODE_TEXT is brotlicffi.BrotliEncoderMode.TEXT
    assert brotlicffi.MODE_FONT is brotlicffi.BrotliEncoderMode.FONT
