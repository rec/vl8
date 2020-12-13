# from numpy.testing import assert_array_equal
# from pydub import AudioSegment
from pathlib import Path
from vl8.dsp import io
from vl8.tasks import combine
import numpy as np
import tdir
import unittest

DIR = Path(__file__).parents[1] / 'sounds'


@tdir(use_dir='test/tasks')
class TestCombine(unittest.TestCase):
    def test_123(self):
        segs, rates = zip(*(io.read(DIR / f'{i}.wav') for i in range(1, 4)))
        assert list(rates) == [44100 / 4] * 3
        assert [s.shape[-1] for s in segs] == [10849, 12172, 11643]
        result = combine.combine(segs, np.float32, gap=44100 // 2)
        assert result is not None
