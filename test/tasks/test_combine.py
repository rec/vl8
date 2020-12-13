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
        result = combine.combine(segs, np.float32, gap=2 * sample_rate)
        assert result is not None
        # io.write(result, '123.wav', sample_rate=sample_rate)

    def test_one(self):
        seg, sample_rate = io.read(DIR / '1.wav')
        io.write(seg, '1.wav', sample_rate)
        # with (DIR / '1.wav').open('rb') as f1, open('1.wav', 'rb') as f2:
        #     assert f1.read() == f2.read()
