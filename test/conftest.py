# -*- coding: utf-8 -*-
import os
import os.path

import pytest

# Statically look for all the files.
curdir = os.path.split(os.path.dirname(__file__))[0]
TEST_DATA_DIR = os.path.join(curdir, 'libbrotli', 'tests', 'testdata')
simple_test_files = [
    os.path.join(TEST_DATA_DIR, p) for p in os.listdir(TEST_DATA_DIR)
]
compressed_simple_test_files = set(
    f for f in simple_test_files if f.endswith('.compressed')
)


@pytest.fixture(params=compressed_simple_test_files)
def simple_compressed_file(request):
    """
    Returns a two-tuple: (uncompressed_file, compressed_file), from the Brotli
    test fixtures.
    """
    file = request.param
    return (file[:-len('.compressed')], file)


@pytest.fixture()
def one_compressed_file():
    return os.path.join(TEST_DATA_DIR, 'alice29.txt')
