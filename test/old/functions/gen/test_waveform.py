from ...assert_files_equal import assert_files_equal
from old.vl8.functions.gen import Sawtooth, Sine, Square, Triangle
import tdir
import unittest

_OVERWRITE_FILES = False


@tdir
class TestSawtooth(unittest.TestCase):
    def test_sawtooth(self):
        result = Sawtooth(duration='0.5 seconds', frequency=100)()
        assert_files_equal('sawtooth-1.wav', result, 44100, _OVERWRITE_FILES)


@tdir
class TestSine(unittest.TestCase):
    def test_sine(self):
        result = Sine(duration='0.5 seconds', frequency=1000)()
        assert_files_equal('sine-1.wav', result, 44100, _OVERWRITE_FILES)


@tdir
class TestSquare(unittest.TestCase):
    def test_square(self):
        result = Square(duration='0.5 seconds', frequency=1000)()
        assert_files_equal('square-1.wav', result, 44100, _OVERWRITE_FILES)


@tdir
class TestSquareDuty(unittest.TestCase):
    def test_square(self):
        result = Square(duration=0.5, duty_cycle='1/8', frequency=1000)()
        assert_files_equal('square-duty.wav', result, 44100, _OVERWRITE_FILES)


@tdir
class TestTriangle(unittest.TestCase):
    def test_triangle(self):
        result = Triangle(duration='0.5 seconds', frequency=1000)()
        assert_files_equal('triangle-1.wav', result, 44100, _OVERWRITE_FILES)
