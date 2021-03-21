from numpy.testing import assert_array_equal
from pathlib import Path
from vl8.dsp.grain import Grain
from vl8.dsp.rand import Rand
import json
import numpy as np
import unittest

RESULTS = Path(__file__).parent / 'grain-results.json'


class TestGrain(unittest.TestCase):
    def data(self, size=20):
        ls = np.linspace(0, size, size, endpoint=False, dtype=np.int32)
        return ls.reshape(2, size // 2)

    def test_default(self):
        g = Grain()
        assert g.stride == 512

        actual = list(g.sizes(4096))
        expected = [
            (0, 1024),
            (512, 1536),
            (1024, 2048),
            (1536, 2560),
            (2048, 3072),
            (2560, 3584),
            (3072, 4096),
            (3584, 4096),
        ]
        assert actual == expected

    def test_simple(self):
        actual = list(Grain(7, 0).chunks(self.data()))
        expected = [
            [[0, 1, 2, 3, 4, 5, 6], [10, 11, 12, 13, 14, 15, 16]],
            [[7, 8, 9], [17, 18, 19]],
        ]
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_array_equal(a, e)

    def test_variation(self):
        grain = Grain(7, 0, rand=Rand(args=(-2, 2), seed=0))
        actual = list(grain.chunks(self.data()))
        expected = [
            [[0, 1, 2, 3, 4, 5, 6, 7], [10, 11, 12, 13, 14, 15, 16, 17]],
            [[8, 9], [18, 19]],
        ]

        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_array_equal(a, e)

    def test_grain(self):
        actual = list(Grain(48).chunks(self.data(1024)))
        expected = json.loads(RESULTS.read_text())
        # RESULTS.write_text(json.dumps(expected, indent=2))
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_array_equal(a, e)
