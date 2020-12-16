# from .assert_files_equal import assert_files_equal

# from vl8.dsp import stretch
from pathlib import Path
from vl8.dsp import io
import os
import tdir
import unittest

DIR = Path(__file__).parent / 'sources'
IS_TRAVIS = os.getenv('TRAVIS', '').lower().startswith('t')
skip_if_travis = unittest.skipIf(IS_TRAVIS, 'Test does not work in travis')


@tdir(use_dir='.')
class TestStretch(unittest.TestCase):
    @skip_if_travis
    def test_pitch_up(self):
        sample_rate = 44100 // 4
        data, rate = io.read(DIR / '2.wav')
        assert rate == sample_rate
        assert data.shape[-1] == 12172

        # stretch.pitch_shift(data, 5, sample_rate)
        # assert_files_equal('2-shift-5.wav', result, sample_rate)
