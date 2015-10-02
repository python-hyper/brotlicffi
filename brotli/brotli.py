# -*- coding: utf-8 -*-
from _brotli import ffi, lib


def decompress(data):
    """
    Decompress a complete Brotli-compressed string.

    :param data: A bytestring containing Brotli-compressed data.
    """
    decoded_size = ffi.new("size_t *")
    rc = lib.BrotliDecompressedSize(len(data), data, decoded_size)
    assert rc == 1
    assert decoded_size[0] > 0

    buffer = ffi.new("char[]", decoded_size[0])
    rc = lib.BrotliDecompressBuffer(len(data), data, decoded_size, buffer)
    assert rc == 1
    assert len(buffer) > 0

    return ffi.string(buffer, decoded_size[0])
