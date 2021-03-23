from fractions import Fraction
from vl8.util.duration import to_seconds, to_samples, to_fraction
import unittest

DATA = '2', '2.3', '23 / 10', '300s', '300ms', '300 samples'


class TestDuration(unittest.TestCase):
    def test_to_seconds(self):
        assert to_seconds('2') == 2
        assert to_seconds('2.3') == 2.3
        assert to_seconds('23 / 10') == Fraction(23, 10)
        assert to_seconds('300s') == 300
        assert to_seconds('300ms') == Fraction(300, 1000)
        with self.assertRaises(ValueError):
            to_seconds('300 samples')
        assert to_seconds('300 samples', 44100) == 300 / 44100

    def test_to_samples(self):
        assert to_samples('2', 44100) == 88200
        assert to_samples('2.3', 44100) == to_fraction(2.3) * 44100
        assert to_samples('300s', 44100) == 300 * 44100
        assert to_samples('300ms', 44100) == 13230
        assert to_samples('300 samples', 44100) == 300
