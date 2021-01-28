Changelog
=========

1.0.9.1 (2021-01-27)
--------------------

- Avoid byte/string comparison warning in error message construction


1.0.9.0 (2021-01-20)
--------------------

- Updated to v1.0.9 of the Brotli library
- Library version now follows Brotli version
- Removed the ``dictionary`` parameter from ``compress`` and ``Compressor``
- **NOTE:** Python 2.7 wheels for Windows likely won't work until
  `google/brotli#848`_ is resolved

.. _google/brotli#848: https://github.com/google/brotli/issues/848

0.8.0 (2020-11-30)
------------------

- Renamed the package on PyPI to ``brotlicffi``, all further updates will be
  published to the new package. Using the ``brotlipy`` is deprecated.
- Changed the importable namespace from ``brotli`` to ``brotlicffi`` to no longer
  conflict with the ``Brotli`` PyPI package.
- Added ``process()`` method to ``Compressor`` and ``Decompressor``.
- Added ``is_finished()`` method to ``Decompressor``.

0.7.0 (2017-05-30)
------------------

- Update to v0.6.0 of the Brotli library.

0.6.0 (2016-09-08)
------------------

- Resolved a bug where ``decompress()`` would return an empty bytestring
  instead of erroring if the provided bytestring was small enough.
- Added the ``finish()`` method to the streaming decompressor.

0.5.1 (2016-08-17)
------------------

- Update to v0.5.2 of the Brotli library.
- Add new exception type (``Error``).
- Add compatibility with C++ brotli library by aliasing ``Error`` to ``error``.
- Extra error checking of input parameters to the compressor.

0.5.0 (2016-08-16)
------------------

- Update to v0.5.0 of the Brotli library.
- Extend one-shot compression API to include all control parameters.
- Added streaming/incremental compression API.
- Added flags to control compression mode.

0.4.0 (2016-08-01)
------------------

Update to v0.4.0 of the Brotli library.

0.3.0 (2016-05-11)
------------------

Update to v0.3.0 of the Brotli library.

0.2.0 (2015-10-05)
------------------

Fix broken ``brotli.compress`` support on Windows.

0.1.3 (2015-10-05)
------------------

- Added basic for ``brotli.compress`` through a C wrapper included in this
  library.
