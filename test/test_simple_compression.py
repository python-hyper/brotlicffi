# -*- coding: utf-8 -*-
"""
test_simple_compression
~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for compression of single chunks.
"""
import brotli

from hypothesis import given
from hypothesis.strategies import binary, integers, sampled_from, one_of


def test_roundtrip_compression_with_files(simple_compressed_file):
    """
    Roundtripping data through the compressor works correctly.
    """
    with open(simple_compressed_file[0], 'rb') as f:
        uncompressed_data = f.read()

    assert brotli.decompress(
        brotli.compress(uncompressed_data)
    ) == uncompressed_data


@given(
    chunk_size=integers(min_value=1, max_value=2**32),
    mode=sampled_from(list(brotli.BrotliEncoderMode)),
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
    c = brotli.Compressor(
        mode=mode, quality=quality, lgwin=lgwin, lgblock=lgblock
    )
    with open(one_compressed_file, 'rb') as f:
        while True:
            next_data = f.read(chunk_size)
            if not next_data:
                break

            compressed_chunks.append(c.compress(next_data))

    compressed_chunks.append(c.finish())
    decompressed = brotli.decompress(b''.join(compressed_chunks))
    with open(one_compressed_file, 'rb') as f:
        assert decompressed == f.read()


@given(
    chunk_size=integers(min_value=1, max_value=2**32),
    mode=sampled_from(list(brotli.BrotliEncoderMode)),
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
    c = brotli.Compressor(
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
    decompressed = brotli.decompress(b''.join(compressed_chunks))
    with open(one_compressed_file, 'rb') as f:
        assert decompressed == f.read()


@given(binary())
def test_compressed_data_roundtrips(s):
    assert brotli.decompress(brotli.compress(s)) == s


@given(binary(), binary())
def test_compressed_data_with_dictionaries(s, dictionary):
    d = brotli.Decompressor(dictionary)
    compressed = brotli.compress(s, dictionary=dictionary)
    uncompressed = d.decompress(compressed)
    assert uncompressed == s
