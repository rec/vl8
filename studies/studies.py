import wavemap
from functools import partial
import numpy as np

SAMPLE_RATE = 44100
DURATION = 5
NSAMPLES = SAMPLE_RATE * DURATION
F_BEGIN = 200
F_END = 400
SCALE = 0.5
DTYPE = np.float64
RATIO = F_END / F_BEGIN
HALF_RATIO = 1 + (RATIO - 1) / 2
CYCLES = 2 * np.pi * DURATION

linspace = partial(np.linspace, endpoint=False, dtype=DTYPE, num=NSAMPLES)
geomspace = partial(np.geomspace, endpoint=False, dtype=DTYPE, num=NSAMPLES)


def write_sin(a, filename):
    wavemap.copy_to(np.sin(a) * SCALE, filename)


begin = linspace(0, F_BEGIN * CYCLES)
end = linspace(0, F_END * CYCLES)

write_sin(begin, 'begin.wav')
write_sin(end, 'end.wav')

write_sin(begin * linspace(1, HALF_RATIO), 'linear.wav')

write_sin(begin * geomspace(1, RATIO), 'geom1.wav')
write_sin(begin * geomspace(1, HALF_RATIO), 'geom2.wav')
write_sin(begin * geomspace(1, np.sqrt(RATIO)), 'geom3.wav')
