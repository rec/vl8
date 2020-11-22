"""
🏃 Run one or more commands 🏃
------------------------------------------------------------------
"""

import aubio
import stroll
import numpy as np

__all__ = 'sorta'
__version__ = '0.1.0'
OUTFILE = '/data/sorta/full.wav'
MAX_FRAME = 4096


def chunks(src):
    duration = src.duration
    for c in src:
        length = c.shape[1]
        if length <= duration:
            yield c
        else:
            yield c[:, :duration]
        duration -= length


def read_file(file=OUTFILE):
    src = aubio.source(file)
    buffer = np.empty(shape=(2, src.duration), dtype=np.float32)
    begin = 0
    for chunk in chunks(src):
        end = begin + chunk.shape[1]
        buffer[:, begin : end] = chunk
        begin = end

    assert end == src.duration
    return buffer


def granules(length=0):
    buffer = read_file(OUTFILE)
    return buffer


if __name__ == '__main__':
    print(read_file().shape)
