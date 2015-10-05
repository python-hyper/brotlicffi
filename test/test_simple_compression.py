# -*- coding: utf-8 -*-
"""
test_simple_compression
~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for compression of single chunks.
"""
import brotli

from hypothesis import given
from hypothesis.strategies import binary


def test_roundtrip_compression_with_files(simple_compressed_file):
    """
    Roundtripping data through the compressor works correctly.
    """
    with open(simple_compressed_file[0], 'rb') as f:
        uncompressed_data = f.read()

    assert brotli.decompress(
        brotli.compress(uncompressed_data)
    ) == uncompressed_data


@given(binary())
def test_compressed_data_roundtrips(s):
    assert brotli.decompress(brotli.compress(s)) == s
