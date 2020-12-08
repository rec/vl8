from vl8 import fader
import unittest


class TestFader(unittest.TestCase):
    def test_immutable(self):
        assert fader.Fader(1000)
