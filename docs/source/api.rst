API Documentation
=================

.. module:: brotlicffi

This section of the documentation covers the API of BrotliCFFI.

Decompression
-------------

.. automethod:: brotlicffi.decompress

.. autoclass:: brotlicffi.Decompressor
  :inherited-members:

Compression
-----------

.. automethod:: brotlicffi.compress

.. autoclass:: brotlicffi.Compressor
   :members:

.. autoclass:: brotlicffi.BrotliEncoderMode
   :members:

.. autodata:: brotlicffi.BROTLI_DEFAULT_MODE

Errors
------

.. autoclass:: brotlicffi.Error

.. autodata:: brotlicffi.error
