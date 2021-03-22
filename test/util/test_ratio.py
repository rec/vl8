from vl8.util import to_fraction
from fractions import Fraction
import unittest


class TestGray(unittest.TestCase):
    def test_error(self):
        with self.assertRaises(TypeError) as m:
            to_fraction('junk')
        assert m.exception.args == ''

    def test_empty(self):
        for x in 0, 0.0, [], [0]:
            assert to_fraction(x) == Fraction()

    def test_simple(self):
        assert to_fraction(f23) is f23
        assert to_fraction((2, 3)) == f23
        assert to_fraction(2 / 3) == f23
