from fractions import Fraction
from old.vl8.types import to_fraction
import itertools
import more_itertools
import unittest


class TestRatio(unittest.TestCase):
    def test_type_error(self):
        with self.assertRaises(TypeError) as m:
            to_fraction(set())
        assert m.exception.args == ("Do not understand set() of type <class 'set'>",)

    def test_value_error(self):
        with self.assertRaises(ValueError) as m:
            to_fraction("junk")
        assert m.exception.args == ("could not convert string to float: 'junk'",)

    def test_empty(self):
        for x in 0, 0.0:
            assert to_fraction(x) == Fraction()

    def test_simple_ratio(self):
        f23 = Fraction(2, 3)
        assert to_fraction(0.66666666) == f23

        for i in f23, "2/3", 2 / 3, "2 / 3", 0.66666666, 0.6666666:
            assert to_fraction(i) == f23

        assert to_fraction(0.666666) == Fraction(333333, 500000)
        assert to_fraction(0.66666) == Fraction(33333, 50000)

    def test_fractions(self):
        MAX = 10000  # Set to 0 for a big test!
        for pp, p in more_itertools.windowed(gen_primes(), 2):
            if MAX and p >= MAX:
                break
            floating = to_fraction(p / pp)
            fractional = Fraction(p, pp)
            if pp > 1000000:
                assert floating == Fraction(766692, 766669)
                assert fractional == Fraction(1000033, 1000003)
                break
            else:
                assert floating == fractional
            pp = p


# https://stackoverflow.com/a/568618/43839
def gen_primes():
    D = {}
    for q in itertools.count(2):
        if q not in D:
            yield q
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
