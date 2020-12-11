from vl8.dsp import envelope
import itertools
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
