from .. import skip
from vl8.util import ffprobe
import unittest

FILE1 = 'test/www-mmsp.ece.mcgill.ca/AFsp/M1F1-int12WE-AFsp.wav'


@skip.if_travis
class TestFfprobe(unittest.TestCase):
    def test_simple(self):
        actual = ffprobe(FILE1)
        from pprint import pprint

        pprint(actual)
        expected = {
            'bitrate': '256 kb/s',
            'channels': '2 channels',
            'duration': '00:00:02.94',
            'encoding': 'pcm_s16le',
            'encoding_data': '([1][0][0][0] / 0x0001)',
            'numbers': 's16',
            'sample_rate': 8000,
        }

        assert actual == expected
