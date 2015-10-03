#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name="brotlipy",
    version="0.1.2",

    description="Python binding to the Brotli library",
    long_description=open("README.rst").read(),
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

    cffi_modules=["src/brotli/build.py:ffi"],

    packages=find_packages('src'),
    package_dir={'': 'src'},

    ext_package="brotli",

    libraries=[
        ("libbrotli", {
            "include_dirs": [
                "libbrotli/enc",
                "libbrotli/dec",
            ],
            "sources": [
                "libbrotli/dec/bit_reader.c",
                "libbrotli/dec/decode.c",
                "libbrotli/dec/huffman.c",
                "libbrotli/dec/state.c",
                "libbrotli/dec/streams.c",
                "libbrotli/dec/dictionary.c",
                "libbrotli/enc/backward_references.cc",
                "libbrotli/enc/histogram.cc",
                "libbrotli/enc/block_splitter.cc",
                "libbrotli/enc/literal_cost.cc",
                "libbrotli/enc/brotli_bit_stream.cc",
                "libbrotli/enc/metablock.cc",
                "libbrotli/enc/encode.cc",
                "libbrotli/enc/static_dict.cc",
                "libbrotli/enc/encode_parallel.cc",
                "libbrotli/enc/streams.cc",
                "libbrotli/enc/entropy_encode.cc",
            ],
        }),
    ],

    zip_safe=False,

    classifiers=[
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ]
)
