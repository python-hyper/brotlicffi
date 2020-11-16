BrotliCFFI: Python CFFI Bindings to the Brotli Compression Algorithm
====================================================================

BrotliCFFI is a collection of `CFFI-based`_ bindings to the `Brotli`_ compression
reference implementation as written by Google. This enables Python software to
easily and quickly work with the Brotli compression algorithm, regardless of
what interpreter is being used.

BrotliCFFI has an identical API to Google's Python C bindings
for the `Brotli`_ library.

.. code-block:: python

    import brotlicffi

    # Decompress a Brotli-compressed payload in one go.
    decompressed_data = brotlicffi.decompress(compressed_data)

    # Alternatively, you can do incremental decompression.
    d = brotlicffi.Decompressor()
    for chunk in chunks_of_compressed_data:
        some_uncompressed_data = d.decompress(chunk)

    remaining_data = d.flush()

    # You can compress data too.
    compressed = brotlicffi.compress(uncompressed_data)

For more details on the API, see :doc:`api`.

.. _CFFI-based: https://cffi.readthedocs.org/en/latest/
.. _Brotli: https://github.com/google/brotli


Documentation
-------------

.. toctree::
   :maxdepth: 2

   installation
   api


License
-------

BrotliCFFI's source code is made available under the MIT license. Brotli itself
is licensed under Version 2.0 of the Apache Software License.
