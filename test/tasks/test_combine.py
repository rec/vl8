from pathlib import Path
from vl8.dsp import io
from vl8.tasks import combine
import numpy as np
import tdir
import unittest

DIR = Path(__file__).parents[1] / 'sounds'


@tdir
class TestCombine(unittest.TestCase):
    def test_123(self):
        sample_rate = 44100 // 4
        segs, rates = zip(*(io.read(DIR / f'{i}.wav') for i in range(1, 4)))
        assert list(rates) == [sample_rate] * 3
        assert [s.shape[-1] for s in segs] == [10849, 12172, 11643]
        result = combine.combine(segs, segs[0].dtype, gap=2 * sample_rate)
        assert result is not None
        io.write('123.wav', result, sample_rate=sample_rate)

    def test_123_float(self):
        sample_rate = 44100 // 4
        segs, rates = zip(*(io.read(DIR / f'{i}.wav') for i in range(1, 4)))
        assert list(rates) == [sample_rate] * 3
        assert [s.shape[-1] for s in segs] == [10849, 12172, 11643]
        result = combine.combine(segs, np.float32, gap=2 * sample_rate)
        assert result is not None
        io.write('123-float.wav', result, sample_rate=sample_rate)

    def test_2(self):
        sample_rate = 44100 // 4
        s, rate = io.read(DIR / '2.wav')
        assert rate == sample_rate
        assert s.shape[-1] == 12172
        result = combine.combine([s], s.dtype, gap=2 * sample_rate)
        assert result is not None
        io.write('2.wav', result, sample_rate=sample_rate)
