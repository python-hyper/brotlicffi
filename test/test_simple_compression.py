# -*- coding: utf-8 -*-
"""
test_simple_compression
~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for compression of single chunks.
"""
import brotlicffi

import pytest

from hypothesis import given, settings
from hypothesis.strategies import binary, integers, sampled_from, one_of


def test_roundtrip_compression_with_files(simple_compressed_file):
    """
    Roundtripping data through the compressor works correctly.
    """
    with open(simple_compressed_file[0], 'rb') as f:
        uncompressed_data = f.read()

    assert brotlicffi.decompress(
        brotlicffi.compress(uncompressed_data)
    ) == uncompressed_data


@pytest.mark.slow
@settings(deadline=None)
@given(
    chunk_size=integers(min_value=1, max_value=2**12),
    mode=sampled_from(list(brotlicffi.BrotliEncoderMode)),
    quality=integers(min_value=0, max_value=11),
    lgwin=integers(min_value=10, max_value=24),
    lgblock=one_of(
        integers(min_value=0, max_value=0),
        integers(min_value=16, max_value=24)
    ),
)
def test_streaming_compression(one_compressed_file,
                               chunk_size,
                               mode,
                               quality,
                               lgwin,
                               lgblock):
    """
    Confirm that the streaming compressor works as expected.
    """
    compressed_chunks = []
    c = brotlicffi.Compressor(
        mode=mode, quality=quality, lgwin=lgwin, lgblock=lgblock
    )
    with open(one_compressed_file, 'rb') as f:
        while True:
            next_data = f.read(chunk_size)
            if not next_data:
                break

            compressed_chunks.append(c.compress(next_data))

    compressed_chunks.append(c.finish())
    decompressed = brotlicffi.decompress(b''.join(compressed_chunks))
    with open(one_compressed_file, 'rb') as f:
        assert decompressed == f.read()


@pytest.mark.slow
@settings(deadline=None)
@given(
    chunk_size=integers(min_value=1, max_value=2**12),
    mode=sampled_from(list(brotlicffi.BrotliEncoderMode)),
    quality=integers(min_value=0, max_value=11),
    lgwin=integers(min_value=10, max_value=24),
    lgblock=one_of(
        integers(min_value=0, max_value=0),
        integers(min_value=16, max_value=24)
    ),
)
def test_streaming_compression_flush(one_compressed_file,
                                     chunk_size,
                                     mode,
                                     quality,
                                     lgwin,
                                     lgblock):
    """
    Confirm that the streaming compressor works as expected, including flushes
    after each chunk.
    """
    compressed_chunks = []
    c = brotlicffi.Compressor(
        mode=mode, quality=quality, lgwin=lgwin, lgblock=lgblock
    )
    with open(one_compressed_file, 'rb') as f:
        while True:
            next_data = f.read(chunk_size)
            if not next_data:
                break

            compressed_chunks.append(c.compress(next_data))
            compressed_chunks.append(c.flush())

    compressed_chunks.append(c.finish())
    decompressed = brotlicffi.decompress(b''.join(compressed_chunks))
    with open(one_compressed_file, 'rb') as f:
        assert decompressed == f.read()


@given(binary())
def test_compressed_data_roundtrips(s):
    assert brotlicffi.decompress(brotlicffi.compress(s)) == s


@given(binary())
def test_process_alias(s):
    c1 = brotlicffi.Compressor()
    c2 = brotlicffi.Compressor()
    d1 = brotlicffi.Decompressor()
    d2 = brotlicffi.Decompressor()
    s1 = c1.compress(s) + c1.finish()
    s2 = c2.process(s) + c2.finish()
    assert (
        (d1.decompress(s1) + d1.finish())
        == (d2.process(s2) + d2.finish())
        == s
    )


@pytest.mark.parametrize(
    "params",
    [
        {"mode": 52},
        {"quality": 52},
        {"lgwin": 52},
        {"lgblock": 52},
    ]
)
def test_bad_compressor_parameters(params):
    with pytest.raises(brotlicffi.error):
        brotlicffi.Compressor(**params)
