from numpy.testing import assert_array_equal
from pathlib import Path
from pydub import AudioSegment
from vl8.sample import Sample
import tdir
import unittest

TEST_FILE = Path(__file__).parent / 'b-4098.wav'


@tdir
class TestSample(unittest.TestCase):
    def test_file(self):
        segment = AudioSegment.from_file(TEST_FILE)
        sample = Sample.read(TEST_FILE)

        assert sample.frame_rate == 44100
        assert sample.data.shape == (2, 4098)
        assert segment._data == sample.data.tobytes('F')
        assert vars(segment) == vars(sample.segment())

        filename = 'result-4098.wav'
        segment.export(filename)

        sample.write(filename)
        sample2 = Sample.read(filename)

        assert_array_equal(sample.data, sample2.data)
