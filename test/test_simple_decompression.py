# -*- coding: utf-8 -*-
"""
test_simple_decompression
~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for decompression of single chunks.
"""
import brotli

import pytest


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


@pytest.mark.parametrize('exception_cls', [brotli.Error, brotli.error])
def test_streaming_decompression_fails_properly_on_garbage(exception_cls):
    """
    Garbage data properly fails decompression.
    """
    o = brotli.Decompressor()
    with pytest.raises(exception_cls):
        o.decompress(b'some random garbage')


@pytest.mark.parametrize('exception_cls', [brotli.Error, brotli.error])
def test_decompression_fails_properly_on_garbage(exception_cls):
    """
    Garbage data properly fails decompression.
    """
    with pytest.raises(exception_cls):
        brotli.decompress(b'some random garbage')
