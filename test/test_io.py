# from numpy.testing import assert_array_equal
from vl8 import npf
from vl8 import util
import aubio
import numpy as np
import tdir
import unittest

DURATION = 2 + 2 * util.MAX_FRAME


@tdir
class TestIO(unittest.TestCase):
    def test_round_trip(self):
        half = DURATION // 2

        b1 = npf.linspace(0, half - 1, half)
        b2 = npf.linspace(half, DURATION - 1, half)

        b1 = b1.reshape(1, half)
        b2 = b2.reshape(1, half)
        b1 = npf.r_[b1, b1]
        b2 = npf.r_[b2, b2]
        util.write('b1.wav', b1)
        util.write('b2.wav', b2)

        c1 = util.read('b1.wav')
        if True:
            return
        assert c1.shape == (2, half)

        total = util.read(('b1.wav', 'b2.wav'))
        assert total.shape == (2, DURATION)

    def test_round_trip_2(self):
        import aubio

        length = 100

        buf = np.linspace(0, length - 1, length, dtype=np.float32)
        buf = buf.reshape(1, length)
        buf = npf.r_[buf, buf]
        assert buf.shape == (2, length)
        if not False:
            sink = aubio.sink('test.wav', channels=2)
            sink.do_multi(buf, length)
            sink.close()

            chunks = list(aubio.source('test.wav'))
            print(len(chunks), chunks[0].shape)

        c1 = util.read('test.wav')
        assert c1.shape == (2, length)

    def test_round_trip_3(self):
        length = 100
        buf = np.zeros((2, length), dtype=np.float32)

        assert buf.shape == (2, length)
        with aubio.sink('test.wav', channels=2) as sink:
            sink.do_multi(buf, length)

        src = aubio.source('test.wav', channels=2)
        assert src.duration == length

        (chunk,) = list(src)

        assert chunk.shape[1] == length
        assert src.duration == length
