from ...assert_files_equal import assert_files_equal
from old.vl8.dsp.rand import Rand
from old.vl8.functions.gen.noise import Noise
import tdir
import unittest


@tdir
class TestNoise(unittest.TestCase):
    def test_noise(self):
        result = Noise(duration="0.5 seconds", rand=Rand(seed=0))()
        assert_files_equal("noise-1.wav", result, 44100)
