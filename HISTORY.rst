Changelog
=========

0.5.1 (2016-08-17)
------------------

- Update to v0.5.2 of the Brotli library.
- Add new exception type (``Error``).
- Add compatiblity with C++ brotli library by aliasing ``Error`` to ``error``.
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
