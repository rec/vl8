from ..assert_files_equal import assert_files_equal
from pathlib import Path
from old.vl8.dsp.data import File
from old.vl8.functions.catenate import Catenate
import tdir
import unittest

DIR = Path(__file__).parents[1] / 'dsp/sources'
FILES = tuple(DIR / f'{i}.wav' for i in range(1, 4))
assert len(FILES) == 3

SAMPLE_RATE = 11025


def catenate(*src, **kwargs):
    return Catenate(**kwargs)(*src)


@tdir
class TestCatenate(unittest.TestCase):
    def test_123_simple(self):
        sources = [File(f) for f in FILES]

        sample_rates = [s.sample_rate for s in sources]
        lengths = [s.nsamples for s in sources]
        nchannels = [s.nchannels for s in sources]
        assert sample_rates == [SAMPLE_RATE, SAMPLE_RATE, SAMPLE_RATE]
        assert lengths == [10849, 12172, 11643]
        assert nchannels == [1, 1, 1]

        result = Catenate(gap=2)(*sources)
        assert_files_equal('123.wav', result, SAMPLE_RATE)

    def test_123_float(self):
        sources = [File(f) for f in FILES]
        result = Catenate(dtype='float32', gap=1)(*sources)
        assert_files_equal('123-float.wav', result, SAMPLE_RATE)

    def test_123_float_fade(self):
        sources = [File(f) for f in FILES]
        result = Catenate(dtype='float32', gap=-1 / 2)(*sources)
        assert_files_equal('123-float-fade.wav', result, SAMPLE_RATE)

    def test_2(self):
        f = File(DIR / '2.wav')
        assert f.nsamples == 12172
        assert f.sample_rate == 11025
        result = Catenate(gap=2)(f)
        assert_files_equal('2.wav', result, SAMPLE_RATE)
