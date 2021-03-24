from ..assert_files_equal import assert_files_equal
from pathlib import Path
from vl8.dsp.data import File
from vl8.dsp.grain import Grain
from vl8.functions.stripe import Stripe
import tdir
import unittest

DIR = Path(__file__).parents[1] / 'dsp/sources'
FILES = tuple(DIR / f'{i}.wav' for i in range(1, 4))
assert len(FILES) == 3

SAMPLE_RATE = 11025


@tdir
class TestStripe(unittest.TestCase):
    def test_123_simple(self):
        sources = [File(f) for f in FILES]
        result = Stripe(grain=Grain(duration='10ms'))(*sources)
        assert_files_equal('stripe-123.wav', result, SAMPLE_RATE)
