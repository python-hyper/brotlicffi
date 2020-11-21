"""A simple project that is compatible with both
'brotli' C bindings and 'brotlicffi' CFFI bindings
"""

import sys

try:
    import brotlicffi as brotli
except ImportError:
    import brotli


def main():
    data = sys.argv[1].encode("utf-8")
    print(f"Compressing data: {data}")

    compressor = brotli.Compressor(mode=brotli.MODE_TEXT)
    compressed = compressor.process(data) + compressor.finish()
    print(f"Compressed data: {compressed}")

    decompressor = brotli.Decompressor()
    decompressed = decompressor.process(compressed) + decompressor.finish()
    print(f"Decompressed data: {decompressed}")


if __name__ == "__main__":
    main()
