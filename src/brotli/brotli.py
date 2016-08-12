# -*- coding: utf-8 -*-
import math
import enum

from ._brotli import ffi, lib


class BrotliEncoderMode(enum.IntEnum):
    """
    Compression modes for the Brotli encoder.

    .. versionadded:: 0.5.0
    """
    #: Default compression mode. The compressor does not know anything in
    #: advance about the properties of the input.
    BROTLI_MODE_GENERIC = lib.BROTLI_MODE_GENERIC

    #: Compression mode for UTF-8 format text input.
    BROTLI_MODE_TEXT = lib.BROTLI_MODE_TEXT

    #: Compression mode used in WOFF 2.0
    BROTLI_MODE_FONT = lib.BROTLI_MODE_FONT


#: The default compression mode for brotli.
BROTLI_DEFAULT_MODE = BrotliEncoderMode(lib.BROTLI_DEFAULT_MODE)


def decompress(data):
    """
    Decompress a complete Brotli-compressed string.

    :param data: A bytestring containing Brotli-compressed data.
    """
    d = Decompressor()
    return d.decompress(data)


def compress(data,
             mode=BROTLI_DEFAULT_MODE,
             quality=lib.BROTLI_DEFAULT_QUALITY,
             lgwin=lib.BROTLI_DEFAULT_WINDOW,
             lgblock=0,
             dictionary=b''):
    """
    Compress a string using Brotli.

    .. versionchanged:: 0.5.0
       Added ``mode``, ``quality``, `lgwin``, ``lgblock``, and ``dictionary``
       parameters.

    :param data: A bytestring containing the data to compress.
    :type data: ``bytes``

    :param mode: The encoder mode.
    :type mode: :class:`BrotliEncoderMode` or ``int``

    :param quality: Controls the compression-speed vs compression-density
        tradeoffs. The higher the quality, the slower the compression. The
        range of this value is 0 to 11.
    :type quality: ``int``

    :param lgwin: The base-2 logarithm of the sliding window size. The range of
        this value is 10 to 24.
    :type lgwin: ``int``

    :param lgblock: The base-2 logarithm of the maximum input block size. The
        range of this value is 16 to 24. If set to 0, the value will be set
        based on ``quality``.
    :type lgblock: ``int``

    :param dictionary: A pre-set dictionary for LZ77. Please use this with
        caution: if a dictionary is used for compression, the same dictionary
        **must** be used for decompression!
    :type dictionary: ``bytes``

    :returns: The compressed bytestring.
    :rtype: ``bytes``
    """
    brotli_encoder = lib.BrotliEncoderCreateInstance(
        ffi.NULL, ffi.NULL, ffi.NULL
    )
    if not brotli_encoder:  # pragma: no cover
        raise RuntimeError("Unable to allocate Brotli encoder!")

    brotli_encoder = ffi.gc(brotli_encoder, lib.BrotliEncoderDestroyInstance)

    # Configure the encoder appropriately.
    lib.BrotliEncoderSetParameter(brotli_encoder, lib.BROTLI_PARAM_MODE, mode)
    lib.BrotliEncoderSetParameter(
        brotli_encoder, lib.BROTLI_PARAM_QUALITY, quality
    )
    lib.BrotliEncoderSetParameter(
        brotli_encoder, lib.BROTLI_PARAM_LGWIN, lgwin
    )
    lib.BrotliEncoderSetParameter(
        brotli_encoder, lib.BROTLI_PARAM_LGBLOCK, lgblock
    )

    if dictionary:
        lib.BrotliEncoderSetCustomDictionary(
            brotli_encoder, len(dictionary), dictionary
        )

    # The 'algorithm' for working out how big to make this buffer is from the
    # Brotli source code, brotlimodule.cc.
    original_output_size = int(math.ceil(len(data) + (len(data) >> 2) + 10240))
    available_out = ffi.new("size_t *")
    available_out[0] = original_output_size
    output_buffer = ffi.new("uint8_t []", available_out[0])
    ptr_to_output_buffer = ffi.new("uint8_t **", output_buffer)
    input_size = ffi.new("size_t *", len(data))
    input_buffer = ffi.new("uint8_t []", data)
    ptr_to_input_buffer = ffi.new("uint8_t **", input_buffer)

    rc = lib.BrotliEncoderCompressStream(
        brotli_encoder,
        lib.BROTLI_OPERATION_FINISH,
        input_size,
        ptr_to_input_buffer,
        available_out,
        ptr_to_output_buffer,
        ffi.NULL
    )
    assert rc == lib.BROTLI_TRUE
    assert lib.BrotliEncoderIsFinished(brotli_encoder) == lib.BROTLI_TRUE
    assert lib.BrotliEncoderHasMoreOutput(brotli_encoder) == lib.BROTLI_FALSE

    size_of_output = original_output_size - available_out[0]
    return ffi.buffer(output_buffer, size_of_output)[:]


class Decompressor(object):
    """
    An object that allows for streaming decompression of Brotli-compressed
    data.

    .. versionchanged:: 0.5.0
       Added ``dictionary`` parameter.

    :param dictionary: A pre-set dictionary for LZ77. Please use this with
        caution: if a dictionary is used for compression, the same dictionary
        **must** be used for decompression!
    :type dictionary: ``bytes``
    """
    _dictionary = None
    _dictionary_size = None

    def __init__(self, dictionary=b''):
        dec = lib.BrotliDecoderCreateInstance(ffi.NULL, ffi.NULL, ffi.NULL)
        self._decoder = ffi.gc(dec, lib.BrotliDecoderDestroyInstance)

        if dictionary:
            self._dictionary = ffi.new("uint8_t []", dictionary)
            self._dictionary_size = len(dictionary)
            lib.BrotliDecoderSetCustomDictionary(
                self._decoder,
                self._dictionary_size,
                self._dictionary
            )

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

            rc = lib.BrotliDecoderDecompressStream(self._decoder,
                                                   available_in,
                                                   next_in,
                                                   available_out,
                                                   next_out,
                                                   ffi.NULL)

            # First, check for errors.
            if rc == lib.BROTLI_DECODER_RESULT_ERROR:
                error_code = lib.BrotliDecoderGetErrorCode(self._decoder)
                error_message = lib.BrotliDecoderErrorString(error_code)
                raise ValueError("Bad bytes: %s" % ffi.string(error_message))

            # Next, copy the result out.
            chunk = ffi.buffer(out_buffer, buffer_size - available_out[0])[:]
            chunks.append(chunk)

            if rc == lib.BROTLI_DECODER_RESULT_NEEDS_MORE_INPUT:
                assert available_in[0] == 0
                break
            elif rc == lib.BROTLI_DECODER_RESULT_SUCCESS:
                break
            else:
                # It's cool if we need more output, we just loop again.
                assert rc == lib.BROTLI_DECODER_RESULT_NEEDS_MORE_OUTPUT

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
