from . import npf
from pathlib import Path
import aubio
import sys

MAX_FRAME = 4096
VERBOSE = True

# https://github.com/aubio/aubio/issues/322
AUBIO_BUG = True


def read(filenames, grain_size=0, duration=0, gap=0):
    if isinstance(filenames, (str, Path)):
        filenames = [filenames]
    filenames = [str(f) for f in filenames]

    assert filenames, 'No filenames'

    if not duration:
        duration = sum(aubio.source(f).duration for f in filenames)
        duration += gap * (len(filenames) - 1)

    fill = grain_size and -duration % grain_size
    if fill:
        buffer = npf.empty(duration + fill)
        buffer[:, -fill:].fill(0)
    else:
        buffer = npf.empty(duration)

    begin = 0
    for filename in filenames:
        log('Reading', filename)
        src = aubio.source(filename)

        for chunk in src:
            if begin >= duration:
                break

            end = min(duration, begin + chunk.shape[1])
            buffer[:, begin:end] = chunk[:, : end - begin]
            begin = end

        begin += gap

    if begin != duration + gap:
        error(f'Wrong duration: {begin} != {duration} + {gap}')

    return buffer


def normalize(buffer):
    buffer /= max(abs(p) for p in (npf.amax(buffer), npf.amin(buffer)))


def write(filename, buffer):
    log('writing', filename)

    channels, nsamples = buffer.shape
    with aubio.sink(filename, channels=channels) as sink:
        for o in range(0, nsamples, MAX_FRAME):
            length = min(MAX_FRAME, nsamples - o)
            buf = buffer[:, o : o + length]
            sink.do_multi(buf, length)


def error(*args, **kwds):
    print(*args, **kwds, file=sys.stderr)


def log(*args, **kwds):
    if VERBOSE:
        error(*args, **kwds)
