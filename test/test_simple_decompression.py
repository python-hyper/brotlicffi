# -*- coding: utf-8 -*-
"""
test_simple_decompression
~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for decompression of single chunks.
"""
import brotli


def test_decompression(simple_compressed_file):
    """
    Decompressing files returns their original form using decompress.
    """
    with open(simple_compressed_file[0], 'rb') as f:
        uncompressed_data = f.read()

    with open(simple_compressed_file[1], 'rb') as f:
        compressed_data = f.read()

    assert brotli.decompress(compressed_data) == uncompressed_data


def test_decompressobj(simple_compressed_file):
    with open(simple_compressed_file[0], 'rb') as f:
        uncompressed_data = f.read()

    with open(simple_compressed_file[1], 'rb') as f:
        compressed_data = f.read()

    o = brotli.Decompressor()
    data = o.decompress(compressed_data)
    data += o.flush()

    assert data == uncompressed_data


def test_drip_feed(simple_compressed_file):
    """
    Sending in the data one byte at a time still works.
    """
    with open(simple_compressed_file[0], 'rb') as f:
        uncompressed_data = f.read()

    with open(simple_compressed_file[1], 'rb') as f:
        compressed_data = f.read()

    outdata = []
    o = brotli.Decompressor()
    for i in range(0, len(compressed_data)):
        outdata.append(o.decompress(compressed_data[i:i+1]))

    outdata.append(o.flush())

    assert b''.join(outdata) == uncompressed_data
