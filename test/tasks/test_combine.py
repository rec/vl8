from pathlib import Path
from pydub import AudioSegment
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
        io.write(result, '123.wav', sample_rate=sample_rate)

    def test_two(self):
        segment = AudioSegment.from_file(DIR / '1.wav')
        segment.export('1.wav', format='wav')
        with (DIR / '1.wav').open('rb') as f1, open('1.wav', 'rb') as f2:
            d1, d2 = f1.read(), f2.read()
            assert len(d1) == len(d2)
            errors = [a for a in enumerate(zip(d1, d2)) if a[1][0] != a[1][1]]
            assert errors == [(4, (134, 133))]
        # AudioSegment changes one bit in the length from the sample

    def NO_test_pydub_24(self):
        # A 24-bit file
        infile = DIR / 'sunnk - skinning gales 07.wav'
        outfile = Path('stereo.wav')
        segment = AudioSegment.from_file(infile)
        segment.export('stereo.wav', format='wav')
        assert infile.read_bytes() == outfile.read_bytes()
