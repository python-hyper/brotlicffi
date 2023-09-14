#!/usr/bin/env python
import os
import re
import platform
import sys
from setuptools import find_packages, setup
from setuptools.command.build_ext import build_ext

base_dir = os.path.dirname(os.path.abspath(__file__))
long_description = (
    open("README.rst").read() + '\n\n' + open("HISTORY.rst").read()
)

with open(os.path.join(base_dir, "src", "brotlicffi", "__init__.py")) as f:
    __version__ = re.search(r"__version__ = \"([^\"]+)\"", f.read()).group(1)


class BuildClibBeforeExt(build_ext):
    """ Setuptools `develop` command (used by `pip install -e .`) only calls
    `build_ext`, unlike `install` which calls `build` and all its related
    sub-commands. Linking the CFFI extension with the libbrotli static library
    fails since the `build_clib` command is not called in the former case.

    This custom `build_ext` class ensures that `build_clib` command is run
    before the CFFI extension module is compiled.

    https://github.com/pypa/pip/issues/4523
    """

    def get_source_files(self):
        filenames = build_ext.get_source_files(self)
        filenames.extend(depends)
        return filenames

    def run(self):
        self.run_command("build_clib")
        build_ext.run(self)


depends = []
libraries = []
USE_SHARED_BROTLI = os.environ.get("USE_SHARED_BROTLI")
if USE_SHARED_BROTLI != "1":
    sources = []

    for root, _, filenames in os.walk("libbrotli/c"):
        root_parts = os.path.split(root)
        if "fuzz" in root_parts or "tools" in root_parts:
            continue
        for filename in filenames:
            relpath = os.path.relpath(os.path.join(root, filename), base_dir)
            if filename.endswith(".h"):
                depends.append(relpath)
            elif filename.endswith(".c"):
                sources.append(relpath)

    libraries = [
        ("libbrotli", {
            "include_dirs": [
                "libbrotli/c/include",
                "libbrotli/c/common",
                "libbrotli/c",
                "src/brotlicffi"
            ],
            "depends": depends,
            "sources": sources,
        }),
    ]

cmdclass = {'build_ext': BuildClibBeforeExt}
if sys.version_info > (3,) and platform.python_implementation() == "CPython":
    try:
        import wheel.bdist_wheel
    except ImportError:
        pass
    else:
        class BDistWheel(wheel.bdist_wheel.bdist_wheel):
            def finalize_options(self):
                self.py_limited_api = "cp3{}".format(sys.version_info[1])
                wheel.bdist_wheel.bdist_wheel.finalize_options(self)
        cmdclass['bdist_wheel'] = BDistWheel

setup(
    name="brotlicffi",
    version=__version__,

    description="Python CFFI bindings to the Brotli library",
    long_description=long_description,
    url="https://github.com/python-hyper/brotlicffi",
    license="MIT",

    author="Cory Benfield",
    author_email="cory@lukasa.co.uk",

    setup_requires=[
        "cffi>=1.0.0",
    ],
    install_requires=[
        "cffi>=1.0.0",
    ],
    python_requires=">=3.7",
    cffi_modules=["src/brotlicffi/_build.py:ffi"],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    ext_package="brotlicffi",
    libraries=libraries,

    zip_safe=False,

    cmdclass=cmdclass,

    classifiers=[
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ]
)
