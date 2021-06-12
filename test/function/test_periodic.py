from vl8.function.periodic import Periodic
import unittest


class TestPeriodic(unittest.TestCase):
    def test_empty(self):
        p = Periodic()
        assert str(p) == (
            "Periodic(duration=None, nchannels=2, sample_rate=44100, "
            "dtype=<class 'numpy.float32'>, cycles=None, "
            "phase=Fraction(0, 1), period=None, frequency=None)"
        )

    def test_simple(self):
        assert Periodic(period=1).frequency == 1
        assert Periodic(period=2).frequency == 0.5
        p = Periodic()
        p.period = 2
        assert p.period == 2
        assert p.actual_duration == 10

        p.frequency = 2
        assert p.period == 0.5
        assert p.actual_duration == 10

        p.duration = 3
        assert p.actual_duration == 3

        p.frequency = 4
        p.cycles = 1
        assert p.actual_duration == 0.25

        p.cycles = 0
        assert p.actual_duration == 0

        p.cycles = None
        assert p.actual_duration == 3
