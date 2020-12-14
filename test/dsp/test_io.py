from numpy.testing import assert_array_equal
from pathlib import Path
from pydub import AudioSegment
from vl8.dsp import io
import numpy as np
import tdir
import unittest

TEST_FILE = Path(__file__).parent / 'b-4098.wav'
DIR = Path(__file__).parent / 'sources'


@tdir
class TestIO(unittest.TestCase):
    def test_file(self):
        length = 4098

        data, sample_rate = io.read(TEST_FILE)

        assert sample_rate == 44100
        assert data.shape == (2, length)
        segment = AudioSegment.from_file(TEST_FILE)
        assert segment._data == data.tobytes('F')

        filename = f'result-{length}.wav'
        io.write(filename, data)
        data2, _ = io.read(filename)

        assert_array_equal(data, data2)

    def test_mono(self):
        length = 7249
        data = np.linspace(0, length - 1, length, dtype=np.int16)
        data = data.reshape(1, length)
        assert data.shape == (1, length,)

        filename = f'result-{length}.wav'
        io.write(filename, data)
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

    def test_two(self):
        infile = DIR / '1.wav'
        outfile = Path('1.wav')
        segment = AudioSegment.from_file(infile)
        segment.export(outfile, format='wav')

        d1 = infile.read_bytes()
        d2 = outfile.read_bytes()
        assert len(d1) == len(d2)
        errors = [a for a in enumerate(zip(d1, d2)) if a[1][0] != a[1][1]]
        assert errors == [(4, (134, 133))]
        # AudioSegment changes one bit in the length from the sample

    def test_three(self):
        infile = DIR / '1.wav'
        outfile = Path('1.wav')
        data, sample_rate = io.read(infile)
        io.write(outfile, data, sample_rate)

        d1 = infile.read_bytes()
        d2 = outfile.read_bytes()
        assert len(d1) == len(d2)
        errors = [a for a in enumerate(zip(d1, d2)) if a[1][0] != a[1][1]]
        assert errors == [(4, (134, 133))]

    def NO_test_pydub_24(self):
        # A 24-bit file
        infile = DIR / 'sunnk - skinning gales 07.wav'
        outfile = Path('stereo.wav')
        segment = AudioSegment.from_file(infile)
        segment.export('stereo.wav', format='wav')
        assert infile.read_bytes() == outfile.read_bytes()
