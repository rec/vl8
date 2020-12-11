from numpy.testing import assert_array_almost_equal
from vl8.dsp.fader import Fader
import numpy as np
import unittest


class TestFader(unittest.TestCase):
    def test_simple(self):
        fader = Fader(4)
        a = np.ones((2, 16), dtype=np.float32) * 100
        actual = fader(a)
        assert a.shape == actual.shape

        channel = (
            [0, 100 / 3, 200 / 3] + [100.0] * 10 + [200 / 3, 100 / 3, 0.0]
        )
        expected = np.array([channel, channel], dtype=np.float32)
        assert_array_almost_equal(expected, actual, decimal=5)
