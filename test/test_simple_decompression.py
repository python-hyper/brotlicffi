# -*- coding: utf-8 -*-
"""
test_simple_decompression
~~~~~~~~~~~~~~~~~~~~~~~~~

Tests for decompression of single chunks.
"""
import brotlicffi

import pytest


def test_decompression(simple_compressed_file):
    """
    Decompressing files returns their original form using decompress.
    """
    with open(simple_compressed_file[0], 'rb') as f:
        uncompressed_data = f.read()

    with open(simple_compressed_file[1], 'rb') as f:
        compressed_data = f.read()

    assert brotlicffi.decompress(compressed_data) == uncompressed_data


def test_decompressobj(simple_compressed_file):
    with open(simple_compressed_file[0], 'rb') as f:
        uncompressed_data = f.read()

    with open(simple_compressed_file[1], 'rb') as f:
        compressed_data = f.read()

    o = brotlicffi.Decompressor()
    data = o.decompress(compressed_data)
    data += o.flush()
    data += o.finish()

    assert data == uncompressed_data


# `more_data_limit` allows testing `decompress(b'')` with and without a limit.
@pytest.mark.parametrize('more_data_limit', [100, None])
def test_decompressobj_with_output_buffer_limit(
    simple_compressed_file, more_data_limit
):
    """
    Test decompression with `output_buffer_limit` set.
    """
    with open(simple_compressed_file[0], 'rb') as f:
        uncompressed_data = f.read()

    with open(simple_compressed_file[1], 'rb') as f:
        compressed_data = f.read()

    o = brotlicffi.Decompressor()
    assert o.can_accept_more_data()
    small_limit = 100
    result = o.decompress(compressed_data, output_buffer_limit=small_limit)
    assert len(result) <= small_limit

    # Ensure `output_buffer_limit` of zero works.
    assert o.decompress(b'', output_buffer_limit=0) == b''

    if o._unconsumed_data:
        with pytest.raises(
            brotlicffi.error,
            match=(
                r"brotli: decoder process called with data when "
                r"'can_accept_more_data\(\)' is False"
            ),
        ):
            o.decompress(b'additional data')

    if not o.is_finished():
        assert not o.can_accept_more_data()

        # Continue decompressing with empty input.
        all_output = [result]
        while not o.can_accept_more_data() and not o.is_finished():
            more_output = o.decompress(
                b'', output_buffer_limit=more_data_limit
            )
            if more_data_limit is not None:
                assert len(more_output) <= more_data_limit
            all_output.append(more_output)
        assert o.can_accept_more_data() or o.is_finished()

        final_result = b''.join(all_output)
        assert final_result == uncompressed_data


def test_drip_feed(simple_compressed_file):
    """
    Sending in the data one byte at a time still works.
    """
    with open(simple_compressed_file[0], 'rb') as f:
        uncompressed_data = f.read()

    with open(simple_compressed_file[1], 'rb') as f:
        compressed_data = f.read()

    outdata = []
    o = brotlicffi.Decompressor()
    for i in range(0, len(compressed_data)):
        assert not o.is_finished()
        outdata.append(o.decompress(compressed_data[i:i+1]))

    assert o.is_finished()
    outdata.append(o.flush())
    assert o.is_finished()
    outdata.append(o.finish())
    assert o.is_finished()

    assert b''.join(outdata) == uncompressed_data


@pytest.mark.parametrize('exception_cls', [brotlicffi.Error, brotlicffi.error])
def test_streaming_decompression_fails_properly_on_garbage(exception_cls):
    """
    Garbage data properly fails decompression.
    """
    o = brotlicffi.Decompressor()
    with pytest.raises(exception_cls):
        o.decompress(b'some random garbage')
    assert not o.is_finished()


@pytest.mark.parametrize('exception_cls', [brotlicffi.Error, brotlicffi.error])
@pytest.mark.parametrize('bogus', (b'some random garbage', b'bogus'))
def test_decompression_fails_properly_on_garbage(bogus, exception_cls):
    """
    Garbage data properly fails decompression.
    """
    with pytest.raises(exception_cls):
        brotlicffi.decompress(bogus)
