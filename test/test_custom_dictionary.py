# -*- coding: utf-8 -*-
"""
Regression tests for Decompressor custom dictionary support (#215).
"""
import brotlicffi


def test_decompressor_accepts_custom_dictionary():
    """
    Constructing Decompressor(dictionary=...) must not raise AttributeError
    for the removed BrotliDecoderSetCustomDictionary API.
    """
    decompressor = brotlicffi.Decompressor(dictionary=b"custom dictionary")
    assert decompressor is not None


def test_decompressor_without_dictionary_still_works():
    """Attaching no dictionary leaves ordinary decompression working."""
    payload = b"hello world from brotlicffi custom dictionary regression"
    compressed = brotlicffi.compress(payload)
    decompressor = brotlicffi.Decompressor()
    assert decompressor.decompress(compressed) + decompressor.finish() == payload
