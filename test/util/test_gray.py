from vl8.util import gray
import itertools
import unittest


class TestGray(unittest.TestCase):
    def test_forward(self):
        actual = list(itertools.islice(gray.iterate(), 16))
        expected = [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8]
        assert actual == expected

    def test_reverse(self):
        actual = list(itertools.islice(gray.iterate(forward=False), 16))
        expected = [0, 1, 3, 2, 7, 6, 4, 5, 15, 14, 12, 13, 8, 9, 11, 10]
        assert actual == expected
