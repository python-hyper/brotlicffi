#!/usr/bin/env python
from setuptools import find_packages, setup

long_description = (
    open("README.rst").read() + '\n\n' + open("HISTORY.rst").read()
)


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

    libraries=[
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
        "Programming Language :: Python :: 3.6",
    ]
)
