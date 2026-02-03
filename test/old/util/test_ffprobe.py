import unittest
from fractions import Fraction

from old.vl8.util import ffprobe

from .. import skip

FILE1 = "test/www-mmsp.ece.mcgill.ca/AFsp/M1F1-int12WE-AFsp.wav"


@skip.if_travis
class TestFfprobe(unittest.TestCase):
    def test_simple(self):
        actual = ffprobe(FILE1)
        from pprint import pprint

        pprint(actual)
        expected = {
            "audio": "pcm_s16le",
            "bitrate": 256000,
            "nchannels": 2,
            "duration": Fraction(147, 50),
            "numbers": "s16",
            "sample_rate": 8000,
        }

        assert actual == expected

    def test_missing(self):
        with self.assertRaises(FileNotFoundError):
            ffprobe("NO-SUCH-FILE.wav")
