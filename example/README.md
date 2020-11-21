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
        "brotli; implementation_name == 'cpython'",
        "brotlicffi; implementation_name != 'cpython'"
    ]
)
```

```
# requirements.txt:
brotli; implementation_name == 'cpython'
brotlicffi; implementation_name != 'cpython'
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
$ python setup.py sdist
$ ls dist/
example-brotli-project-0.1.0.tar.gz
```

### Installing on CPython

Run `python:3.7-slim` Docker image to test against CPython

```
$ docker run --rm -it -v $(pwd)/dist:/dist python:3.7-slim /bin/bash
```

Install the example project

```
$ python -m pip install /dist/example-brotli-project-0.1.0.tar.gz
Processing /dist/example-brotli-project-0.1.0.tar.gz
Collecting brotli
  Downloading Brotli-1.0.9-cp37-cp37-manylinux1_x86_64.whl (357 kB)
     |████████████████████████████████| 357 kB 1.9 MB/s 
Building wheels for collected packages: example-brotli-project
  Building wheel for example-brotli-project (setup.py) ... done
  Created wheel for example-brotli-project: filename=example_brotli_project-0.1.0-py3-none-any.whl size=1976 sha256=b94975444c08cf82f395c8277e29b5b6f3b3270dd4f7d224482e4493be89c6bd
  Stored in directory: /root/.cache/pip/wheels/be/67/36/911a88789436560de345984e6c4c3785098e98b92dcbab5980
Successfully built example-brotli-project
Installing collected packages: brotli, example-brotli-project
Successfully installed brotli-1.0.9 example-brotli-project-0.1.0
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

Run `pypy:3.7-slim` Docker image to test against PyPy

```
$ docker run --rm -it -v $(pwd)/dist:/dist pypy:3.7-slim /bin/bash
$ pypy -m pip install /dist/example-brotli-project-0.1.0.tar.gz
Processing /dist/example-brotli-project-0.1.0.tar.gz
Collecting brotlicffi
  Downloading brotlicffi-0.8.0-pp37-pypy37_pp73-manylinux1_x86_64.whl (341 kB)
     |████████████████████████████████| 341 kB 2.8 MB/s 
Requirement already satisfied: cffi>=1.0.0 in /opt/pypy/lib_pypy (from brotlicffi->example-brotli-project==0.1.0) (1.14.2)
Building wheels for collected packages: example-brotli-project
  Building wheel for example-brotli-project (setup.py) ... done
  Created wheel for example-brotli-project: filename=example_brotli_project-0.1.0-py3-none-any.whl size=1976 sha256=566f5bfb3a0d74d11485b02b929a09d6e6cc8bab7c409cf30ff50f2067692356
  Stored in directory: /root/.cache/pip/wheels/cb/e1/0f/337346ea74252e5b652824bb0f2fc82e81208f9f8e3de42465
Successfully built example-brotli-project
Installing collected packages: brotlicffi, example-brotli-project
Successfully installed brotlicffi-0.8.0 example-brotli-project-0.1.0
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
