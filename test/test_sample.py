from numpy.testing import assert_array_equal
from pathlib import Path
from pydub import AudioSegment
from vl8.sample import Sample
import numpy as np
import tdir
import unittest

TEST_FILE = Path(__file__).parent / 'b-4098.wav'
SAMPLE_RATE = 44100


@tdir
class TestSample(unittest.TestCase):
    def test_file(self):
        length = 4098

        segment = AudioSegment.from_file(TEST_FILE)
        sample = Sample.read(TEST_FILE)

        assert sample.frame_rate == SAMPLE_RATE
        assert sample.data.shape == (2, length)
        assert segment._data == sample.data.tobytes('F')
        assert vars(segment) == vars(sample.segment())

        filename = f'result-{length}.wav'
        sample.write(filename)
        sample2 = Sample.read(filename)

        assert_array_equal(sample.data, sample2.data)

    def test_mono(self):
        length = 7249
        data = np.linspace(0, length - 1, length, dtype=np.int16)
        sample = Sample(data, SAMPLE_RATE)

        assert len(sample.data.shape) == 2

        filename = f'result-{length}.wav'
        sample.write(filename)
        sample2 = Sample.read(filename)
        assert sample.data.shape == sample2.data.shape
        assert_array_equal(sample.data, sample2.data)
