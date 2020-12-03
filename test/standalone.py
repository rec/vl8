import aubio
import numpy as np
import os

FRAME = 4096
REMOVE = True


def write_empty(duration):
    buffer = np.zeros((2, duration), dtype=np.float32)

    filename = f'b-{duration}.wav'
    with aubio.sink(filename, channels=2) as sink:
        for o in range(0, duration, FRAME):
            length = min(FRAME, duration - o)
            buf = buffer[:, o : o + length]
            sink.do_multi(buf, length)

    src = aubio.source(filename)
    assert sum(i.shape[1] for i in src) == duration
    if REMOVE:
        os.remove(filename)
    return src.duration


def test_crash(start, count):
    bad = 0
    for d in range(start, start + count):
        if d:
            duration = write_empty(d)
            if d != duration:
                # print(d - start, d, duration)
                bad += 1

    print('---->', count, bad)


if __name__ == '__main__':
    test_crash(0, 129)
    test_crash(FRAME, 128)
