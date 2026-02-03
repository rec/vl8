import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal

from old.vl8.dsp.fader import Fader


class TestFader(unittest.TestCase):
    def test_simple(self):
        fader = Fader(4)
        a = np.ones((2, 16), dtype=np.float32) * 100
        actual = np.zeros_like(a)
        fader(a, actual)
        assert a.shape == actual.shape

        ramp = [0, 100 / 3, 200 / 3]
        channel = ramp + [100.0] * 10 + ramp[::-1]

        expected = np.array([channel, channel], dtype=np.float32)
        assert_array_almost_equal(expected, actual, decimal=5)

    def test_target(self):
        fader = Fader(4, 6)
        a = np.ones((2, 16), dtype=np.float32) * 100
        target = np.linspace(0, 100, 32, endpoint=True, dtype=np.float32)
        target = target.reshape(2, 16)
        fader(a, target)
        expected = [
            [
                0.0,
                36.559143,
                73.118286,
                109.67742,
                112.90323,
                116.12903,
                119.35484,
                122.58064,
                125.80645,
                129.03226,
                132.25806,
                115.48387,
                98.70969,
                81.935486,
                65.161285,
                48.387096,
            ],
            [
                51.612904,
                88.17204,
                124.731186,
                161.29031,
                164.51613,
                167.74194,
                170.96774,
                174.19354,
                177.41936,
                180.64517,
                183.87097,
                167.09677,
                150.32259,
                133.54839,
                116.77419,
                100.0,
            ],
        ]
        expected = np.array(expected, dtype=np.float32)
        print(target)
        assert_array_almost_equal(expected, target, decimal=5)
