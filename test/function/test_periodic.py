from vl8.function.periodic import Periodic
import unittest


class TestPeriodic(unittest.TestCase):
    def test_empty(self):
        p = Periodic()
        assert str(p) == (
            "Periodic(duration=0, nchannels=2, sample_rate=44100, "
            "dtype=<class 'numpy.float32'>, cycles=None, phase=0, "
            "period=None, frequency=None)"
        )

    def test_simple(self):
        assert Periodic(period=1).frequency == 1
        assert Periodic(period=2).frequency == 0.5
        p = Periodic()
        p.period = 2
        assert p.period == 2

        p.frequency = 2
        assert p.period == 0.5
