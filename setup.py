#!/usr/bin/env python
import os.path

from setuptools import setup

import brotli


def here(*paths):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), *paths))


setup(
    name=brotli.__title__,
    version=brotli.__version__,

    description=brotli.__summary__,
    long_description=open("README.rst").read(),
    url=brotli.__uri__,
    license=brotli.__license__,

    author=brotli.__author__,
    author_email=brotli.__email__,

    setup_requires=[
        "cffi>=1.0.0",
    ],
    install_requires=[
        "cffi>=1.0.0",
    ],

    cffi_modules=["brotli/build.py:ffi"],

    packages=[
        "brotli",
    ],

    ext_package="brotli",

    libraries=[
        ("libbrotli", {
            "include_dirs": [
                here("libbrotli/enc"),
                here("libbrotli/dec"),
            ],
            "sources": [
                here("libbrotli/", s) for s in [
                    "dec/bit_reader.c",
                    "dec/decode.c",
                    "dec/huffman.c",
                    "dec/state.c",
                    "dec/streams.c",
                    "dec/dictionary.c",
                    "enc/backward_references.cc",
                    "enc/histogram.cc",
                    "enc/block_splitter.cc",
                    "enc/literal_cost.cc",
                    "enc/brotli_bit_stream.cc",
                    "enc/metablock.cc",
                    "enc/encode.cc",
                    "enc/static_dict.cc",
                    "enc/encode_parallel.cc",
                    "enc/streams.cc",
                    "enc/entropy_encode.cc"
                ]
            ],
        }),
    ],

    zip_safe=False,

    classifiers=[
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
    ]
)
