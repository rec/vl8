from ...assert_files_equal import assert_files_equal
from vl8.functions.gen.waveform import Sawtooth, Sine
import tdir
import unittest

_OVERWRITE_FILES = False


@tdir
class TestSawtooth(unittest.TestCase):
    def test_sawtooth(self):
        result = Sawtooth(duration='0.5 seconds', frequency=100)()
        assert_files_equal('sawtooth-1.wav', result, 44100, _OVERWRITE_FILES)


@tdir
class TestSine(unittest.TestCase):
    def test_sine(self):
        result = Sine(duration='0.5 seconds', frequency=1000)()
        assert_files_equal('sine-1.wav', result, 44100, _OVERWRITE_FILES)
