from ..assert_files_equal import assert_files_equal
from pathlib import Path
from vl8.dsp import io
from vl8.functions import cat
import numpy as np
import tdir
import unittest

DIR = Path(__file__).parents[1] / 'dsp/sources'
FILES = tuple(DIR / f'{i}.wav' for i in range(1, 4))


@tdir
class TestCat(unittest.TestCase):
    def test_123(self):
        sample_rate = 44100 // 4
        segs, rates = zip(*(io.read(f) for f in FILES))
        assert list(rates) == [sample_rate] * 3
        assert [s.shape[-1] for s in segs] == [10849, 12172, 11643]
        result = cat.cat(segs, segs[0].dtype, gap=2 * sample_rate)
        assert_files_equal('123.wav', result, sample_rate)

    def test_123_float(self):
        sample_rate = 44100 // 4
        segs, rates = zip(*(io.read(f) for f in FILES))
        assert list(rates) == [sample_rate] * 3
        assert [s.shape[-1] for s in segs] == [10849, 12172, 11643]
        result = cat.cat(segs, np.float32, gap=1 * sample_rate)
        assert_files_equal('123-float.wav', result, sample_rate)

    def test_123_float_fade(self):
        sample_rate = 44100 // 4
        segs, rates = zip(*(io.read(f) for f in FILES))
        assert list(rates) == [sample_rate] * 3
        assert [s.shape[-1] for s in segs] == [10849, 12172, 11643]
        result = cat.cat(segs, np.float32, gap=-sample_rate // 2)
        assert_files_equal('123-float-fade.wav', result, sample_rate)

    def test_2(self):
        sample_rate = 44100 // 4
        s, rate = io.read(DIR / '2.wav')
        assert rate == sample_rate
        assert s.shape[-1] == 12172
        result = cat.cat([s], s.dtype, gap=2 * sample_rate)
        assert_files_equal('2.wav', result, sample_rate)
