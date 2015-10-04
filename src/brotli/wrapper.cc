/* C-compatible wrapper for the Brotli compressor. */
#include "../enc/encode.h"

#if defined(__cplusplus) || defined(c_plusplus)
extern "C" {
#endif

int BrotliCompressBuffer(size_t input_size,
                         const uint8_t* input_buffer,
                         size_t* encoded_size,
                         uint8_t* encoded_buffer) {
  brotli::BrotliParams params;
  int ok = brotli::BrotliCompressBuffer(params,
                                        input_size,
                                        input_buffer,
                                        encoded_size,
                                        encoded_buffer);
  return ok;
}

#if defined(__cplusplus) || defined(c_plusplus)
}    /* extern "C" */
#endif
