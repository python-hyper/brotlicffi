# -*- coding: utf-8 -*-
import sys

from cffi import FFI
ffi = FFI()

libraries = ['libbrotli']
if 'win32' not in str(sys.platform).lower():
    libraries.append('stdc++')


ffi.set_source(
    "_brotli",
    """#include <dec/decode.h>
       #include <wrapper.h>
    """,
    libraries=libraries,
    include_dirs=["libbrotli", "src/brotli"]
)

ffi.cdef("""
    /* dec/state.h */
    typedef ... BrotliState;

    /* Allocating function pointer. Function MUST return 0 in the case of
       failure. Otherwise it MUST return a valid pointer to a memory region of
       at least size length. Neither items nor size are allowed to be 0.
       opaque argument is a pointer provided by client and could be used to
       bind function to specific object (memory pool). */
    typedef void* (*brotli_alloc_func)(void* opaque, size_t size);

    /* Deallocating function pointer. Function SHOULD be no-op in the case the
       address is 0. */
    typedef void (*brotli_free_func)(void* opaque, void* address);

    /* Creates the instance of BrotliState and initializes it. alloc_func and
       free_func MUST be both zero or both non-zero. In the case they are both
       zero, default memory allocators are used. opaque is passed to alloc_func
       and free_func when they are called. */
    BrotliState* BrotliCreateState(brotli_alloc_func alloc_func,
                                   brotli_free_func free_func,
                                   void* opaque);

    /* Deinitializes and frees BrotliState instance. */
    void BrotliDestroyState(BrotliState* state);


    /* dec/decode.h */

    typedef enum {
      /* Decoding error, e.g. corrupt input or no memory */
      BROTLI_RESULT_ERROR = 0,
      /* Successfully completely done */
      BROTLI_RESULT_SUCCESS = 1,
      /* Partially done, but must be called again with more input */
      BROTLI_RESULT_NEEDS_MORE_INPUT = 2,
      /* Partially done, but must be called again with more output */
      BROTLI_RESULT_NEEDS_MORE_OUTPUT = 3
    } BrotliResult;

    /* Sets *decoded_size to the decompressed size of the given encoded */
    /* stream. This function only works if the encoded buffer has a single */
    /* meta block, or if it has two meta-blocks, where the first is */
    /* uncompressed and the second is empty. */
    /* Returns 1 on success, 0 on failure. */
    int BrotliDecompressedSize(size_t encoded_size,
                               const uint8_t* encoded_buffer,
                               size_t* decoded_size);

    /* Decompresses the data in encoded_buffer into decoded_buffer, and sets */
    /* *decoded_size to the decompressed length. */
    /* Returns 0 if there was either a bit stream error or memory allocation */
    /* error, and 1 otherwise. */
    /* If decoded size is zero, returns 1 and keeps decoded_buffer */
    /* unchanged. */
    BrotliResult BrotliDecompressBuffer(size_t encoded_size,
                                        const uint8_t* encoded_buffer,
                                        size_t* decoded_size,
                                        uint8_t* decoded_buffer);

    /* Decompresses the data. Supports partial input and output.
    /*
    /* Must be called with an allocated input buffer in *next_in and an
    /* allocated output buffer in *next_out. The values *available_in and
    /* *available_out must specify the allocated size in *next_in and *next_out
    /* respectively.
    /*
    /* After each call, *available_in will be decremented by the amount of
    /* input bytes consumed, and the *next_in pointer will be incremented by
    /* that amount. Similarly, *available_out will be decremented by the amount
    /* of output bytes written, and the *next_out pointer will be incremented
    /* by that amount. total_out, if it is not a null-pointer, will be set to
    /* the number of bytes decompressed since the last state initialization.
    /*
    /* Input is never overconsumed, so next_in and available_in could be passed
    /* to the next consumer after decoding is complete. */
    BrotliResult BrotliDecompressStream(size_t* available_in,
                                        const uint8_t** next_in,
                                        size_t* available_out,
                                        uint8_t** next_out,
                                        size_t* total_out,
                                        BrotliState* s);

    /* Fills the new state with a dictionary for LZ77, warming up the
       ringbuffer, e.g. for custom static dictionaries for data formats.
       Not to be confused with the built-in transformable dictionary of Brotli.
       The dictionary must exist in memory until decoding is done and is owned
       by the caller. To use:
       -initialize state with BrotliStateInit
       -use BrotliSetCustomDictionary
       -use BrotliDecompressBufferStreaming
       -clean up with BrotliStateCleanup
    */
    void BrotliSetCustomDictionary(
        size_t size, const uint8_t* dict, BrotliState* s);


    /* wrapper.h */
    int BrotliCompressBuffer(size_t input_size,
                             const uint8_t* input_buffer,
                             size_t* encoded_size,
                             uint8_t* encoded_buffer);
""")

if __name__ == '__main__':
    ffi.compile()
