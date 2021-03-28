from ...assert_files_equal import assert_files_equal
from vl8.functions.gen.sawtooth import Sawtooth
import tdir
import unittest


@tdir
class TestSawtooth(unittest.TestCase):
    def test_sawtooth(self):
        result = Sawtooth(duration='0.5 seconds', frequency=100)()
        assert_files_equal('sawtooth-1.wav', result, 44100)
