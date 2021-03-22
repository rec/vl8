from fractions import Fraction
from vl8.util.ratio import to_fraction
import unittest


class TestGray(unittest.TestCase):
    def test_error(self):
        with self.assertRaises(TypeError) as m:
            to_fraction('junk')
        assert m.exception.args == (
            "Do not understand junk of type <class 'str'>",
        )

    def test_empty(self):
        for x in 0, 0.0, [], [0]:
            assert to_fraction(x) == Fraction()

    def test_simple(self):
        f23 = Fraction(2, 3)
        assert to_fraction(f23) is f23
        assert to_fraction([2, 3]) == f23
        assert to_fraction(2 / 3) == f23
        assert to_fraction(0.66666666) == f23
        assert to_fraction(0.6666666) == f23
        assert to_fraction(0.666666) == Fraction(333333, 500000)
        assert to_fraction(0.66666) == Fraction(33333, 50000)
