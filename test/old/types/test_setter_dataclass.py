import unittest
from fractions import Fraction
from typing import Optional

from old.vl8.types import setter_dataclass, types


class TestSetterDataclass(unittest.TestCase):
    def test_setter_dataclass(self):
        @setter_dataclass
        class One:
            one: types.Numeric
            two: str = "a"
            three: types.NumericSequence = None
            four: types.Numeric | None = None
            five: types.Numeric | None = "23.5"

        one = One("2 / 3", "b", ["4.25", 12])
        assert one.one == Fraction(2, 3)
        assert one.three == [4.25, 12]
        assert one.four is None
        assert one.five == 23.5
