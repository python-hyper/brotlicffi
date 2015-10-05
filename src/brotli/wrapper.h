/* C-compatible wrapper for the Brotli compressor. */
#if defined(__cplusplus) || defined(c_plusplus)
extern "C" {
#endif

int BrotliCompressBuffer(size_t input_size,
                         const uint8_t* input_buffer,
                         size_t* encoded_size,
                         uint8_t* encoded_buffer);

#if defined(__cplusplus) || defined(c_plusplus)
}    /* extern "C" */
#endif