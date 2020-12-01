from vl8 import npf
import unittest


class TestNpf(unittest.TestCase):
    def test_stereo(self):
        a = npf.ones(5)
        assert a.shape == (2, 5)
        assert all(all(j == 1.0 for j in i) for i in a)
