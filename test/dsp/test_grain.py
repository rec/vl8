from numpy.testing import assert_array_equal
from random import Random
from vl8.dsp.grain import Grain
import itertools
import numpy as np
import unittest


class TestGrain(unittest.TestCase):
    def test_default(self):
        g = Grain()
        assert g.stride == 512

        actual = list(itertools.islice(g.sizes(), 7))
        expected = [
            (0, 1024),
            (512, 1536),
            (1024, 2048),
            (1536, 2560),
            (2048, 3072),
            (2560, 3584),
            (3072, 4096),
        ]
        assert actual == expected

    def test_grains(self):
        size = 20
        data = np.linspace(0, size, size, dtype=np.int32).reshape(2, size // 2)

        grain = Grain(7, 4)
        actual = list(grain.grains(data))
        print(actual)
        assert len(actual) == 4

        expected = [
            [[0, 1, 2, 3, 4, 5, 6], [10, 11, 12, 13, 14, 15, 16]],
            [[3, 4, 5, 6, 7, 8, 9], [13, 14, 15, 16, 17, 18, 20]],
            [[6, 7, 8, 9], [16, 17, 18, 20]],
            [[9], [20]],
        ]
        assert_array_equal(actual[0], np.array(expected[0], dtype=np.int32))
        assert_array_equal(actual[1], np.array(expected[1], dtype=np.int32))
        assert_array_equal(actual[2], np.array(expected[2], dtype=np.int32))
        assert_array_equal(actual[3], np.array(expected[3], dtype=np.int32))

    def test_variation(self):
        size = 20
        data = np.linspace(0, size, size, dtype=np.int32).reshape(2, size // 2)

        rand = Random(0)

        grain = Grain(7, 4, variation=2)
        actual = list(grain.grains(data, rand))
        assert len(actual) == 3

        expected = [
            [[0, 1, 2, 3, 4, 5, 6, 7], [10, 11, 12, 13, 14, 15, 16, 17]],
            [[4, 5, 6, 7, 8, 9], [14, 15, 16, 17, 18, 20]],
            [[8, 9], [18, 20]],
        ]
        assert_array_equal(actual[0], np.array(expected[0], dtype=np.int32))
        assert_array_equal(actual[1], np.array(expected[1], dtype=np.int32))
        assert_array_equal(actual[2], np.array(expected[2], dtype=np.int32))
