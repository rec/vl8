import unittest
from pathlib import Path

import tdir

from old.vl8.dsp import io

from .. import skip

DIR = Path(__file__).parent / "sources"


@tdir(use_dir=".")
class TestStretch(unittest.TestCase):
    @skip.if_travis
    def test_pitch_up(self):
        sample_rate = 44100 // 4
        data, rate = io.read(DIR / "2.wav")
        assert rate == sample_rate
        assert data.shape[-1] == 12172

        # stretch.pitch_shift(data, 5, sample_rate)
        # assert_files_equal('2-shift-5.wav', result, sample_rate)
