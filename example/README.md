# Example Project using C and CFFI Brotli Bindings

This simple example project shows how to include
`brotlicffi` into projects supporting both CPython
and other Python implementations like PyPy.

Basically it boils down to these two steps:

Include the two dependencies in your `install_requires`/`requirements.txt`:

```python
# install_requires:
from setuptools import setup

setup(
    ...,
    install_requires=[
        "brotli; platform_python_implementation == 'CPython'",
        "brotlicffi; platform_python_implementation != 'CPython'"
    ]
)
```

```
# requirements.txt:
brotli; platform_python_implementation == 'CPython'
brotlicffi; platform_python_implementation != 'CPython'
```

...then you can import the bindings in your project like so:

```python
try:
    import brotlicffi as brotli
except ImportError:
    import brotli
```

It should be that simple! Now let's see our example project in action:

## Installing on CPython and PyPy

Build the project sdist locally

```
$ cd example/
$ pipx run build
$ ls dist/
example_brotli_project-0.1.0-py3-none-any.whl  example_brotli_project-0.1.0.tar.gz
```

### Installing on CPython

Run `python:3.12-slim` Docker image to test against CPython

```
$ docker run --rm -it -v $(pwd)/dist:/dist python:3.12-slim /bin/bash
```

Install the example project

```
$ python -m pip install /dist/example_brotli_project-0.1.0-py3-none-any.whl
Processing /dist/example_brotli_project-0.1.0-py3-none-any.whl
Collecting brotli (from example-brotli-project==0.1.0)
  Downloading Brotli-1.1.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (5.5 kB)
Downloading Brotli-1.1.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.9/2.9 MB 10.5 MB/s eta 0:00:00
Installing collected packages: brotli, example-brotli-project
Successfully installed brotli-1.1.0 example-brotli-project-0.1.0
```

Notice that `Brotli` is installed from PyPI instead of `brotlicffi` on CPython.

Now run the program and see the output:

```
$ example-brotli-project "Hello, world!"
Compressing data: b'Hello, world!'
Compressed data: b'\x0b\x06\x80Hello, world!\x03'
Decompressed data: b'Hello, world!'
```

### Installing on PyPy

Run `pypy:3.10-slim` Docker image to test against PyPy

```
$ docker run --rm -it -v $(pwd)/dist:/dist pypy:3.10-slim /bin/bash
$ pypy -m pip install /dist/example_brotli_project-0.1.0-py3-none-any.whl 
Processing /dist/example_brotli_project-0.1.0-py3-none-any.whl
Collecting brotlicffi
  Downloading brotlicffi-1.1.0.0-pp310-pypy310_pp73-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (378 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 378.6/378.6 kB 4.8 MB/s eta 0:00:00
Requirement already satisfied: cffi>=1.0.0 in /opt/pypy/lib/pypy3.10 (from brotlicffi->example-brotli-project==0.1.0) (1.17.0.dev0)
Installing collected packages: brotlicffi, example-brotli-project
Successfully installed brotlicffi-1.1.0.0 example-brotli-project-0.1.0
```

Notice now that `brotlicffi` is installed from PyPI instead of `Brotli` on CPython.

Now run the program and see the output:

```
$ example-brotli-project "Hello, world!"
Compressing data: b'Hello, world!'
Compressed data: b'\x0b\x06\x80Hello, world!\x03'
Decompressed data: b'Hello, world!'
```

Identical output compared to CPython! :tada:
