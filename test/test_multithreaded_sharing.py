""" Test multithreaded sharing of Compressor and Decompressor instances

Originally written by Eugene Kliuchnikov at Google for the brotli
Python bindings under an MIT license.

"""
import queue
import random
import threading
import time

import brotlicffi


def make_input(size):
    abc = [bytes([b]) for b in b"abcdefghijklmnopqrstuvwxyz"]
    abc_cap = [bytes([b]) for b in b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    num_words_by_len = [0, 25, 100, 175, 1700, 1000, 1000, 1000]
    word_set = set()
    rng = random.Random()
    rng.seed(2025)
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


def _thread_concurrent_process(compressor, results):
    time.sleep(0.01)
    try:
        _ = compressor.process(b"whatever")
    except brotlicffi.error:
        results.put(2)


def _thread_concurrent_flush(compressor, results):
    time.sleep(0.02)
    try:
        _ = compressor.flush()
    except brotlicffi.error:
        results.put(3)


def _thread_concurrent_finish(compressor, results):
    time.sleep(0.03)
    try:
        _ = compressor.finish()
    except brotlicffi.error:
        results.put(4)


def test_concurrency():
    original = make_input(2 * 1024 * 1024)
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
            target=_thread_concurrent_process, args=(compressor, results)
        )
    )
    threads.append(
        threading.Thread(
            target=_thread_concurrent_flush, args=(compressor, results)
        )
    )
    threads.append(
        threading.Thread(
            target=_thread_concurrent_finish, args=(compressor, results)
        )
    )
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert sorted(list(results.queue)) == [1, 2, 3, 4]
