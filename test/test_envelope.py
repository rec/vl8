from numpy.testing import assert_array_equal
from vl8.dsp import envelope
import itertools
import numpy as np
import unittest


class TestSegments(unittest.TestCase):
    def test_empty(self):
        segs = envelope._segments([0], [128], None)
        s = list(itertools.islice(segs, 4))
        assert s == [(0, 0, 128)] * 4

    def test_single(self):
        segs = envelope._segments([0, 4], [128], None)
        s = list(itertools.islice(segs, 4))
        assert s == [(0, 4, 128), (4, 0, 128)] * 2

    def test_three(self):
        segs = envelope._segments([0, 2, 4], [128], None)
        s = list(itertools.islice(segs, 6))
        assert s == [(0, 2, 128), (2, 4, 128), (4, 0, 128)] * 2


class TestEnvelope(unittest.TestCase):
    def test_simple(self):
        env = envelope.Envelope([12, 70, 211], [10, 2])
        a = np.ones((2, 8), dtype=np.int32) * 10
        actual = env(a)
        assert a.shape == actual.shape

        # TODO: actually validate that this is the right answer
        channel = [120, 180, 240, 310, 370, 440, 500, 570]
        expected = np.array([channel, channel], dtype=np.int32)
        assert_array_equal(expected, actual)
