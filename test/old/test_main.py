from . import assert_files_equal
from pathlib import Path
from old.vl8.__main__ import main
import tdir
import unittest

DIR = Path(__file__).parent / "dsp/sources"
FILES = tuple(DIR / f"{i}.wav" for i in range(1, 4))
assert len(FILES) == 3

SAMPLE_RATE = 11025
FILENAME = "cat-one-two-three.wav"


@tdir
class TestMain(unittest.TestCase):
    def test_main(self):
        args = [str(f) for f in FILES] + ["-o" + FILENAME]
        main(args)
        assert Path(FILENAME).exists()
        assert_files_equal.assert_equal(FILENAME)
