#!/usr/bin/env python
import os
from setuptools import find_packages, setup
from setuptools.command.build_ext import build_ext

long_description = (
    open("README.rst").read() + '\n\n' + open("HISTORY.rst").read()
)

class BuildClibBeforeExt(build_ext):
    """ Setuptools `develop` command (used by `pip install -e .`) only calls
    `build_ext`, unlike `install` which calls `build` and all its related
    sub-commands. Linking the CFFI extension with the libbrotli static library
    fails since the `build_clib` command is not called in the former case.

    This custom `build_ext` class ensures that `build_clib` command is run
    before the CFFI extension module is compiled.

    https://github.com/pypa/pip/issues/4523
    """

    def run(self):
        self.run_command("build_clib")
        build_ext.run(self)

libraries = []
USE_SHARED_BROTLI = os.environ.get("USE_SHARED_BROTLI")
if USE_SHARED_BROTLI != "1":
    libraries = [
        ("libbrotli", {
            "include_dirs": [
                "libbrotli/include",
                "libbrotli/",
                "src/brotli"
            ],
            "sources": [
                'libbrotli/common/dictionary.c',
                'libbrotli/dec/huffman.c',
                'libbrotli/dec/bit_reader.c',
                'libbrotli/dec/decode.c',
                'libbrotli/dec/state.c',
                'libbrotli/enc/backward_references.c',
                'libbrotli/enc/backward_references_hq.c',
                'libbrotli/enc/bit_cost.c',
                'libbrotli/enc/block_splitter.c',
                'libbrotli/enc/histogram.c',
                'libbrotli/enc/memory.c',
                'libbrotli/enc/literal_cost.c',
                'libbrotli/enc/brotli_bit_stream.c',
                'libbrotli/enc/compress_fragment_two_pass.c',
                'libbrotli/enc/compress_fragment.c',
                'libbrotli/enc/cluster.c',
                'libbrotli/enc/utf8_util.c',
                'libbrotli/enc/encode.c',
                'libbrotli/enc/metablock.c',
                'libbrotli/enc/static_dict.c',
                'libbrotli/enc/dictionary_hash.c',
                'libbrotli/enc/entropy_encode.c'
            ]
        }),
    ]

setup(
    name="brotlipy",
    version="0.7.0",

    description="Python binding to the Brotli library",
    long_description=long_description,
    url="https://github.com/python-hyper/brotlipy/",
    license="MIT",

    author="Cory Benfield",
    author_email="cory@lukasa.co.uk",

    setup_requires=[
        "cffi>=1.0.0",
    ],
    install_requires=[
        "cffi>=1.0.0",
    ],
    extras_require={
        ':python_version == "2.7" or python_version == "3.3"': ['enum34>=1.0.4, <2'],
    },

    cffi_modules=["src/brotli/build.py:ffi"],

    packages=find_packages('src'),
    package_dir={'': 'src'},

    ext_package="brotli",

    libraries=libraries,

    zip_safe=False,

    cmdclass={
        'build_ext': BuildClibBeforeExt,
    },

    classifiers=[
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
