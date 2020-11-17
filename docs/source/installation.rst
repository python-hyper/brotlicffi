Installation
============

Installing BrotliCFFI couldn't be easier:

.. code-block:: bash

    $ python -m pip install brotlicffi

On OS X and Windows this should succeed without difficulty. On Linux, the above
command has a few dependencies: mostly, you need a C compiler, the Python
header files, and libffi.

On Debian-based systems, you can obtain these files by running:

.. code-block:: bash

    $ apt-get install build-essential python-dev libffi-dev

On Red Hat-based systems, you can obtain these files by running:

.. code-block:: bash

    $ yum install gcc libffi-devel python-devel
