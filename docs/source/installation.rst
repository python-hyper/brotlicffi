Installation
============

Installing Brotlipy couldn't be easier:

.. code-block:: bash

    $ pip install brotlipy

On OS X this should succeed without difficulty. On Windows, this should also be
no problem for Python 3, though Python 2 is unsupported due to compiler
limitations. On Linux, the above command has a few dependencies: mostly, you
need a C compiler, the Python header files, and libffi.

On Debian-based systems, you can obtain these files by running:

.. code-block:: bash

    $ apt-get install build-essential python-dev libffi-dev

On Red Hat-based systems, you can obtain these files by running:

.. code-block:: bash

    $ yum install gcc libffi-devel python-devel
