import aubio
import numpy as np
import sys

MAX_FRAME = 4096
FLOAT = np.float32
VERBOSE = True


def empty(length, channels=2):
    return np.empty(shape=(channels, length), dtype=FLOAT)


def zeros(length, channels=2):
    return np.zeros(shape=(channels, length), dtype=FLOAT)


def read(filename, grain_size=0, duration=0):
    log('reading', filename)
    src = aubio.source(str(filename))

    duration = duration or src.duration
    if grain_size:
        duration += -duration % grain_size

    buffer = empty(duration)

    begin = 0
    for chunk in src:
        if begin >= duration:
            break

        end = min(duration, begin + chunk.shape[1])
        buffer[:, begin:end] = chunk[:, : end - begin]
        begin = end
    else:
        if begin < duration:
            buffer[:, begin:].fill(0)

    return buffer


def normalize(buffer):
    buffer /= max(abs(p) for p in (np.amax(buffer), np.amin(buffer)))


def write(filename, buffer):
    log('writing', filename)

    channels, nsamples = buffer.shape
    sink = aubio.sink(filename, channels=channels)

    for o in range(0, nsamples, MAX_FRAME):
        length = min(MAX_FRAME, nsamples - o)
        sink.do_multi(buffer[:, o : o + length], length)


def log(*args, **kwds):
    if VERBOSE:
        print(*args, **kwds, file=sys.stderr)
