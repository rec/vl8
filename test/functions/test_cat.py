from ..assert_files_equal import assert_files_equal
from pathlib import Path
from vl8.dsp.data import File
from vl8.functions import cat
import tdir
import unittest

DIR = Path(__file__).parents[1] / 'dsp/sources'
FILES = tuple(DIR / f'{i}.wav' for i in range(1, 4))
assert len(FILES) == 3

SAMPLE_RATE = 11025


@tdir
class TestCat(unittest.TestCase):
    def test_123_simple(self):
        sources = [File(f) for f in FILES]

        sample_rates = [s.sample_rate for s in sources]
        sample_counts = [s.sample_count for s in sources]
        channels = [s.channels for s in sources]
        assert sample_rates == [SAMPLE_RATE, SAMPLE_RATE, SAMPLE_RATE]
        assert sample_counts == [10849, 12172, 11643]
        assert channels == [1, 1, 1]

        result = cat.cat(*sources, gap=2)
        assert_files_equal('123.wav', result, SAMPLE_RATE)

    def test_123_float(self):
        sources = [File(f) for f in FILES]
        result = cat.cat(*sources, dtype='float32', gap=1)
        assert_files_equal('123-float.wav', result, SAMPLE_RATE)

    def test_123_float_fade(self):
        sources = [File(f) for f in FILES]
        result = cat.cat(*sources, dtype='float32', gap=-1 / 2)
        assert_files_equal('123-float-fade.wav', result, SAMPLE_RATE)

    def test_2(self):
        f = File(DIR / '2.wav')
        assert f.sample_count == 12172
        assert f.sample_rate == 11025
        result = cat.cat(f, gap=2)
        assert_files_equal('2.wav', result, SAMPLE_RATE)
