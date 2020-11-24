import aubio
import functools

MAX_FRAME = 4096
FLOAT = np.float32


def empty(length, channels=2):
    return np.empty(shape=(channels, length), dtype=FLOAT)


def zeros(length, channels=2):
    return np.zeros(shape=(channels, length), dtype=FLOAT)


def read(filename, grain_size=0):
    src = aubio.source(filename)

    duration = src.duration
    if grain_size:
        duration += (-duration % grain_size)
    buffer = empty(duration)

    begin = 0
    for chunk in src:
        end = min(duration, begin + chunk.shape[1])
        buffer[:, begin : end] = chunk[:, : end - begin]
        begin = end

    return buffer


def write(buffer, filename):
    channels, nsamples = buffer.shape
    sink = aubio.sink(filename, channels=channels)

    for o in range(0, nsamples, MAX_FRAME):
        length = min(MAX_FRAME, nsamples - o)
        sink.do_multi(buffer[:, o:o+length], length)


if __name__ == '__main__':
    read_all()
