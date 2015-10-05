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
    assert rc == 1

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
        self.state = ffi.new("BrotliState *")
        lib.BrotliStateInit(self.state)

    def decompress(self, data):
        """
        Decompress part of a complete Brotli-compressed string.

        :param data: A bytestring containing Brotli-compressed data.
        :returns: A bytestring containing the decompressed data.
        """
        chunks = []
        index_ptr = ffi.new("int *")
        index_ptr[0] = 0
        exceptions = []

        @ffi.callback("int(void *, uint8_t *, size_t)")
        def _brotli_in(index_ptr, buf, length):
            try:
                buf = ffi.buffer(buf, length)
                index_ptr = ffi.cast("int *", index_ptr)
                index = index_ptr[0]
                data_to_write = data[index:index+length]
                buf[0:len(data_to_write)] = data_to_write
                index_ptr[0] += len(data_to_write)
                return len(data_to_write)
            except Exception as e:  # pragma: no cover
                exceptions.append(e)
                return 0

        @ffi.callback("int(void *, uint8_t *, size_t)")
        def _brotli_out(data_ptr, buf, length):
            try:
                chunks.append(ffi.buffer(ffi.cast("char *", buf), length)[:])
                return length
            except Exception as e:  # pragma: no cover
                exceptions.append(e)
                return 0

        brotli_input = ffi.new("BrotliInput *", [_brotli_in, index_ptr])
        brotli_output = ffi.new("BrotliOutput *", [_brotli_out, ffi.NULL])

        while index_ptr[0] < len(data):
            rc = lib.BrotliDecompressStreaming(
                brotli_input[0], brotli_output[0], 0, self.state
            )
            assert rc > 0
            if exceptions:  # pragma: no cover
                raise exceptions[0]

        return b''.join(chunks)

    def flush(self):
        """
        Complete the decompression, return whatever data is remaining to be
        decompressed.

        This action also resets the decompression state, allowing the
        decompressor to be used again.

        :returns: A bytestring containing the remaining decompressed data.
        """
        chunks = []
        exceptions = []

        @ffi.callback("int(void *, uint8_t *, size_t)")
        def _brotli_in(index_ptr, buf, length):
            return 0

        @ffi.callback("int(void *, uint8_t *, size_t)")
        def _brotli_out(data_ptr, buf, length):
            try:
                chunks.append(ffi.buffer(ffi.cast("char *", buf), length)[:])
                return length
            except Exception as e:  # pragma: no cover
                exceptions.append(e)
                return 0

        brotli_input = ffi.new("BrotliInput *", [_brotli_in, ffi.NULL])
        brotli_output = ffi.new("BrotliOutput *", [_brotli_out, ffi.NULL])

        while True:
            rc = lib.BrotliDecompressStreaming(
                brotli_input[0], brotli_output[0], 1, self.state
            )
            assert rc > 0
            if exceptions:  # pragma: no cover
                raise exceptions[0]
            if rc < 3:  # pragma: no cover
                break

        return b''.join(chunks)
