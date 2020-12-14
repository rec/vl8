from pathlib import Path
from vl8.dsp import io
from vl8.tasks import combine
import numpy as np
import tdir
import unittest

DIR = Path(__file__).parents[1] / 'sounds'
FILES = tuple(DIR / f'{i}.wav' for i in range(1, 4))


@tdir(use_dir=None and '.')
class TestCombine(unittest.TestCase):
    def test_123(self):
        sample_rate = 44100 // 4
        segs, rates = zip(*(io.read(f) for f in FILES))
        assert list(rates) == [sample_rate] * 3
        assert [s.shape[-1] for s in segs] == [10849, 12172, 11643]
        result = combine.combine(segs, segs[0].dtype, gap=2 * sample_rate)
        _test('123.wav', result, sample_rate)

    def test_123_float(self):
        sample_rate = 44100 // 4
        segs, rates = zip(*(io.read(f) for f in FILES))
        assert list(rates) == [sample_rate] * 3
        assert [s.shape[-1] for s in segs] == [10849, 12172, 11643]
        result = combine.combine(segs, np.float32, gap=1 * sample_rate)
        io.write('123-float.wav', result, sample_rate=sample_rate)

    def test_123_float_fade(self):
        sample_rate = 44100 // 4
        segs, rates = zip(*(io.read(f) for f in FILES))
        assert list(rates) == [sample_rate] * 3
        assert [s.shape[-1] for s in segs] == [10849, 12172, 11643]
        result = combine.combine(segs, np.float32, gap=-sample_rate // 2)
        io.write('123-float-fade.wav', result, sample_rate=sample_rate)

    def test_2(self):
        sample_rate = 44100 // 4
        s, rate = io.read(DIR / '2.wav')
        assert rate == sample_rate
        assert s.shape[-1] == 12172
        result = combine.combine([s], s.dtype, gap=2 * sample_rate)
        io.write('2.wav', result, sample_rate=sample_rate)


def _test(filename, result, sample_rate):
    io.write(filename, result, sample_rate=sample_rate)
    rfile = Path(__file__).parent / 'results' / filename
    d1, d2 = Path(filename).read_bytes(), rfile.read_bytes()
    assert d1 == d2
