from numpy.testing import assert_array_equal
from vl8.dsp.grain import Grain
import itertools
import numpy as np
import unittest


class TestGrain(unittest.TestCase):
    def test_default(self):
        g = Grain()
        assert g.stride == 3 * 256
        assert g.fade == 256

        sizes = list(itertools.islice(g.sizes(), 4))
        assert sizes == [(0, 1024), (768, 1792), (1536, 2560), (2304, 3328)]

    def test_grains(self):
        size = 20
        data = np.linspace(0, size, size, dtype=np.int32).reshape(2, size // 2)

        grain = Grain(7)
        g1, g2 = list(grain.grains(data))

        a1 = [[0, 1, 2, 3, 4, 5, 6], [10, 11, 12, 13, 14, 15, 16]]
        a2 = [[5, 6, 7, 8, 9], [15, 16, 17, 18, 20]]

        assert_array_equal(g1, np.array(a1, dtype=np.int32))
        assert_array_equal(g2, np.array(a2, dtype=np.int32))

    def test_variation(self):
        size = 20
        data = np.linspace(0, size, size, dtype=np.int32).reshape(2, size // 2)

        grain = Grain(7, variation=0.3, seed=0)
        g1, g2 = list(grain.grains(data))

        a1 = [[0, 1, 2, 3, 4, 5, 6, 7], [10, 11, 12, 13, 14, 15, 16, 17]]
        a2 = [[6, 7, 8, 9], [16, 17, 18, 20]]

        assert_array_equal(g1, np.array(a1, dtype=np.int32))
        assert_array_equal(g2, np.array(a2, dtype=np.int32))
