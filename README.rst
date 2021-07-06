BrotliCFFI
==========

.. image:: https://img.shields.io/pypi/v/brotlicffi
    :alt: Version
    :target: https://pypi.org/project/brotlicffi

.. image:: https://img.shields.io/conda/vn/conda-forge/brotlicffi
    :alt: Version-Conda
    :target: https://anaconda.org/conda-forge/brotlicffi

.. image:: https://pepy.tech/badge/brotlicffi
    :alt: Downloads
    :target: https://pepy.tech/project/brotlicffi

.. image:: https://img.shields.io/github/workflow/status/python-hyper/brotlicffi/CI/master
    :alt: CI Status
    :target: https://github.com/python-hyper/brotlicffi/actions

This library contains Python CFFI bindings for the reference Brotli encoder/decoder,
`available here`_. This allows Python software to use the Brotli compression
algorithm directly from Python code.

Install from PyPI:

.. code-block::

    $ python -m pip install brotlicffi

Install from Conda:

.. code-block::

    $ conda install -c conda-forge brotlicffi

To use it simply, try this:

.. code-block:: python

    import brotlicffi
    data = brotlicffi.decompress(compressed_data)

More information can be found `in the documentation`_.

.. _available here: https://github.com/google/brotli
.. _in the documentation: https://brotlipy.readthedocs.org

Using BrotliCFFI in Projects
----------------------------

The API is 100% compatible with the `Brotli Python C bindings`_.
We recommend installing the C bindings on CPython and the CFFI
bindings everywhere else (PyPy, etc)

Essentially you use requirements like this:

 .. code-block:: python

    install_requires=[
        "brotli; platform_python_implementation == 'CPython'",
        "brotlicffi; platform_python_implementation != 'CPython'"
    ]

and then import the correct Brotli library like so:

 .. code-block:: python

    try:
        import brotlicffi as brotli
    except ImportError:
        import brotli

We provide an `example project`_ that shows how to use both
libraries together to support Brotli with multiple Python implementations.

.. _Brotli Python C bindings: https://pypi.org/project/Brotli
.. _example project: https://github.com/python-hyper/brotlipy/tree/master/example

License
-------

The source code of BrotliCFFI is available under the MIT license. Brotli itself
is made available under the Version 2.0 of the Apache Software License. See the
LICENSE and libbrotli/LICENSE files for more information.

Authors
-------

BrotliCFFI/brotlipy was authored by Cory Benfield and
is currently maintained by Seth Michael Larson.
