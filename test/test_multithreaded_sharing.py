""" Test multithreaded sharing of Compressor and Decompressor instances

Originally written by Eugene Kliuchnikov at Google for the brotli
Python bindings under an MIT license.

"""
import queue
import random
import threading
import time

import brotlicffi


def make_compress_input(size):
    abc = [bytes([b]) for b in b"abcdefghijklmnopqrstuvwxyz"]
    abc_cap = [bytes([b]) for b in b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    num_words_by_len = [0, 25, 100, 175, 1700, 1000, 1000, 1000]
    word_set = set()
    rng = random.Random()
    rng.seed(0x4d3d3d3)
    words_by_len = [[]]
    for word_len in range(1, len(num_words_by_len)):
        num_words = num_words_by_len[word_len]
        words = []
        for _ in range(num_words):
            while True:
                word = b"".join(
                    [rng.choice(abc_cap)]
                    + [rng.choice(abc) for _ in range(word_len - 1)]
                )
                if word not in word_set:
                    word_set.add(word)
                    words.append(word)
                    break
        words_by_len.append(words)
    total_size = 0
    out = []
    while total_size < size:
        word_len = rng.choice(range(1, len(num_words_by_len)))
        word = rng.choice(words_by_len[word_len])
        total_size += len(word)
        out.append(word)
    return b"".join(out)


def _thread_compress(original, compressor, results):
    compressed = compressor.process(original)
    compressed += compressor.finish()
    results.put(1)


def _thread_concurrent_process_compress(compressor, results):
    time.sleep(0.001)
    try:
        _ = compressor.process(b"whatever")
    except brotlicffi.error:
        results.put(2)


def _thread_concurrent_flush_compress(compressor, results):
    time.sleep(0.002)
    try:
        _ = compressor.flush()
    except brotlicffi.error:
        results.put(3)


def _thread_concurrent_finish_compress(compressor, results):
    time.sleep(0.003)
    try:
        _ = compressor.finish()
    except brotlicffi.error:
        results.put(4)


def test_compress_concurrency():
    original = make_compress_input(2 * 1024 * 1024)
    compressor = brotlicffi.Compressor(quality=9)
    results = queue.Queue()
    threads = []
    threads.append(
        threading.Thread(
            target=_thread_compress, args=(original, compressor, results)
        )
    )
    threads.append(
        threading.Thread(
            target=_thread_concurrent_process_compress,
            args=(compressor, results)
        )
    )
    threads.append(
        threading.Thread(
            target=_thread_concurrent_flush_compress,
            args=(compressor, results)
        )
    )
    threads.append(
        threading.Thread(
            target=_thread_concurrent_finish_compress,
            args=(compressor, results)
        )
    )
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert sorted(list(results.queue)) == [1, 2, 3, 4]


def make_decompress_input(size):
    compressor = brotlicffi.Compressor(quality=1)
    prologue = compressor.process(b'b')
    prologue += compressor.flush()
    filler = compressor.process(b'c')
    filler += compressor.flush()
    epilogue = compressor.finish()
    return b''.join(
        [prologue] + [filler] * (size // len(filler)) + [epilogue])


def _thread_decompress(compressed, decompressor, results):
    _ = decompressor.process(compressed)
    if decompressor.is_finished():
        results.put(1)


def _thread_concurrent_process(decompressor, results):
    time.sleep(0.001)
    try:
        _ = decompressor.process(b'')
    except brotlicffi.error:
        results.put(2)


def _thread_concurrent_can_accept_more_data(decompressor, results):
    time.sleep(0.002)
    try:
        _ = decompressor.can_accept_more_data()
    except brotlicffi.error:
        results.put(3)


def _thread_concurrent_is_finished(decompressor, results):
    time.sleep(0.03)
    try:
        _ = decompressor.is_finished()
    except brotlicffi.error:
        results.put(4)


def test_decompressor_concurrency():
    compressed = make_decompress_input(16 * 1024 * 1024)
    decompressor = brotlicffi.Decompressor()
    results = queue.Queue()
    threads = []
    threads.append(
        threading.Thread(
            target=_thread_decompress, args=(compressed, decompressor, results)
        )
    )
    threads.append(
        threading.Thread(
            target=_thread_concurrent_process, args=(decompressor, results)
        )
    )
    threads.append(
        threading.Thread(
            target=_thread_concurrent_can_accept_more_data,
            args=(decompressor, results),
        )
    )
    threads.append(
        threading.Thread(
            target=_thread_concurrent_is_finished, args=(decompressor, results)
        )
    )
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert sorted(list(results.queue)) == [1, 2, 3, 4]
