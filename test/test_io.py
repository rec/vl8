from numpy.testing import assert_array_equal
from vl8 import util
import numpy as np
import tdir
import unittest

DURATION = 2 + 2 * util.MAX_FRAME


@tdir
class TestIO(unittest.TestCase):
    def NO_test_round_trip(self):
        half = DURATION // 2

        b1 = util.linspace(0, half - 1, half)
        b2 = util.linspace(half, DURATION - 1, half, dtype='int32')

        b1 = b1.reshape(1, half)
        b2 = b2.reshape(1, half)
        b1 = np.r_[b1, b1]
        b2 = np.r_[b2, b2]
        util.write('b1.wav', b1)
        util.write('b2.wav', b2)

        assert_array_equal(b1, util.read('b1.wav'))
        assert_array_equal(b2, util.read('b2.wav'))
