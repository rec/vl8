from numpy.testing import assert_array_equal
from pathlib import Path
from pydub import AudioSegment
from vl8.sample import Sample
import numpy as np
import tdir
import unittest

TEST_FILE = Path(__file__).parent / 'b-4098.wav'


@tdir
class TestSample(unittest.TestCase):
    def test_file(self):
        length = 4098

        segment = AudioSegment.from_file(TEST_FILE)
        sample = Sample.read(TEST_FILE)

        assert sample.frame_rate == 44100
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
        sample = Sample(data)

        assert sample.data.shape == (1, length)

        filename = f'result-{length}.wav'
        sample.write(filename)
        sample2 = Sample.read(filename)
        assert sample.data.shape == sample2.data.shape
        assert_array_equal(sample.data, sample2.data)

    def test_mono_stereo(self):
        length = 4
        mono = Sample(np.linspace(0, length - 1, length, dtype=np.int16))
        stereo = Sample(np.ones((2, length), dtype=np.int16))

        assert mono.data.shape == (1, length)

        stereo.data += mono.data
        expected = np.array([[1, 2, 3, 4], [1, 2, 3, 4]], dtype=np.int16)
        assert_array_equal(stereo.data, expected)
