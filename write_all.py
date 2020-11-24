"""
🏃 Run one or more commands 🏃
------------------------------------------------------------------
"""

import aubio
import numpy as np
import stroll

__all__ = 'sorta'
__version__ = '0.1.0'
OUTFILE = '/data/sorta/full.wav'
MAX_FRAME = 4096


def granules(source, length=0):
    pass


def read_all():
    files = [str(i) for i in stroll('/data/sorta', suffix='.wav')]

    duration = sum(aubio.source(f).duration for f in files)
    buffer = np.empty(shape=(2, duration), dtype=np.float32)

    offset = 0
    for f in files:
        print(f)
        src = aubio.source(f)

        remaining = src.duration
        for chunk in src:
            channels, length = chunk.shape
            assert channels == 2

            if length <= remaining:
                source = chunk
            else:
                # The chunk sample length is always even, so sometimes the
                # chunk # length is one longer than the file duration, which I
                # take as authoritative.
                print(f'{length} <= {remaining}')
                source = source[:, :remaining]
                length = remaining

            buffer[:, offset : offset + length] = source
            offset += length
            remaining -= length

    print('Writing', OUTFILE)
    sink = aubio.sink(OUTFILE, channels=2)

    for offset in range(0, duration, MAX_FRAME):
        length = min(MAX_FRAME, duration - offset)
        sink.do_multi(buffer[:, offset : offset + length], length)


if __name__ == '__main__':
    read_all()
