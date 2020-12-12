from numpy.testing import assert_array_equal
from pathlib import Path
from pydub import AudioSegment
from vl8.dsp import io
import numpy as np
import tdir
import unittest

TEST_FILE = Path(__file__).parent / 'b-4098.wav'


@tdir
class TestSample(unittest.TestCase):
    def test_file(self):
        length = 4098

        data, sample_rate = io.read(TEST_FILE)

        assert sample_rate == 44100
        assert data.shape == (2, length)
        segment = AudioSegment.from_file(TEST_FILE)
        assert segment._data == data.tobytes('F')

        filename = f'result-{length}.wav'
        io.write(data, filename)
        data2, _ = io.read(filename)

        assert_array_equal(data, data2)

    def test_mono(self):
        length = 7249
        data = np.linspace(0, length - 1, length, dtype=np.int16)
        data = data.reshape(1, length)
        assert data.shape == (1, length,)

        filename = f'result-{length}.wav'
        io.write(data, filename)
        data2, _ = io.read(filename)
        assert_array_equal(data, data2)

    def test_mono_stereo(self):
        length = 4
        mono = np.linspace(0, length - 1, length, dtype=np.int16)
        mono = mono.reshape(1, length)
        stereo = np.ones((2, length), dtype=np.int16)

        assert mono.shape == (1, length)

        stereo += mono
        expected = np.array([[1, 2, 3, 4], [1, 2, 3, 4]], dtype=np.int16)
        assert_array_equal(stereo.data, expected)
