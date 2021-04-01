from dataclasses import dataclass
from fractions import Fraction
from vl8.types import types, prop
import unittest


class TestProp(unittest.TestCase):
    def test_prop(self):
        @dataclass
        class One:
            one: types.Numeric
            two: str = 'a'
            three: types.NumericSequence = None

        prop(One)

        one = One('2 / 3', 'b', ['4.25', 12])
        assert one.one == Fraction(2, 3)
        assert one.three == [4.25, 12]
