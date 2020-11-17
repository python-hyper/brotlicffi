BrotliCFFI
==========

This library contains Python CFFI bindings for the reference Brotli encoder/decoder,
`available here`_. This allows Python software to use the Brotli compression
algorithm directly from Python code.

To use it simply, try this:

.. code-block:: python

    import brotlicffi
    data = brotlicffi.decompress(compressed_data)

More information can be found `in the documentation`_.

.. _available here: https://github.com/google/brotli
.. _in the documentation: https://brotlipy.readthedocs.org

License
-------

The source code of BrotliCFFI is available under the MIT license. Brotli itself
is made available under the Version 2.0 of the Apache Software License. See the
LICENSE and libbrotli/LICENSE files for more information.

Authors
-------

BrotliCFFI/brotlipy was authored by Cory Benfield and
is currently maintained by Seth Michael Larson.
