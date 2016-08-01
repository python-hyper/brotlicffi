# -*- coding: utf-8 -*-
import math

from ._brotli import ffi, lib


def decompress(data):
    """
    Decompress a complete Brotli-compressed string.

    :param data: A bytestring containing Brotli-compressed data.
    """
    decoded_size = ffi.new("size_t *")
    rc = lib.BrotliDecompressedSize(len(data), data, decoded_size)
    assert rc == 1

    buffer = ffi.new("char[]", decoded_size[0])
    rc = lib.BrotliDecompressBuffer(len(data), data, decoded_size, buffer)
    if rc == lib.BROTLI_RESULT_ERROR:
        raise ValueError("Bad bytes")

    return ffi.buffer(buffer, decoded_size[0])[:]


def compress(data):
    """
    Compress a string using Brotli.

    :param data: A bytestring containing the data to compress.
    """
    # The 'algorithm' for working out how big to make this buffer is from the
    # Brotli source code, brotlimodule.cc.
    compressed_size = ffi.new("size_t *")
    compressed_size[0] = int(math.ceil(1.2 * len(data) + 10240))
    buffer = ffi.new("char[]", compressed_size[0])

    rc = lib.BrotliCompressBuffer(len(data), data, compressed_size, buffer)
    assert rc == 1

    return ffi.buffer(buffer, compressed_size[0])[:]


class Decompressor(object):
    """
    An object that allows for streaming decompression of Brotli-compressed
    data.
    """
    def __init__(self):
        self.state = lib.BrotliCreateState(ffi.NULL, ffi.NULL, ffi.NULL)
        assert self.state

    def decompress(self, data):
        """
        Decompress part of a complete Brotli-compressed string.

        :param data: A bytestring containing Brotli-compressed data.
        :returns: A bytestring containing the decompressed data.
        """
        chunks = []

        available_in = ffi.new("size_t *", len(data))
        in_buffer = ffi.new("uint8_t[]", data)
        next_in = ffi.new("uint8_t **", in_buffer)

        while True:
            # Allocate a buffer that's hopefully overlarge, but if it's not we
            # don't mind: we'll spin around again.
            buffer_size = 5 * len(data)
            available_out = ffi.new("size_t *", buffer_size)
            out_buffer = ffi.new("uint8_t[]", buffer_size)
            next_out = ffi.new("uint8_t **", out_buffer)

            rc = lib.BrotliDecompressStream(available_in,
                                            next_in,
                                            available_out,
                                            next_out,
                                            ffi.NULL,
                                            self.state)

            # First, check for errors.
            if rc == lib.BROTLI_RESULT_ERROR:
                raise ValueError("Bad bytes")

            # Next, copy the result out.
            chunk = ffi.buffer(out_buffer, buffer_size - available_out[0])[:]
            chunks.append(chunk)

            if rc == lib.BROTLI_RESULT_NEEDS_MORE_INPUT:
                assert available_in[0] == 0
                break
            elif rc == lib.BROTLI_RESULT_SUCCESS:
                break
            else:
                # It's cool if we need more output, we just loop again.
                assert rc == lib.BROTLI_RESULT_NEEDS_MORE_OUTPUT

        return b''.join(chunks)

    def flush(self):
        """
        Complete the decompression, return whatever data is remaining to be
        decompressed.

        This action also resets the decompression state, allowing the
        decompressor to be used again.

        .. deprecated:: 0.4.0

            This method is no longer required, as decompress() will now
            decompress eagerly.

        :returns: A bytestring containing the remaining decompressed data.
        """

        return b''
