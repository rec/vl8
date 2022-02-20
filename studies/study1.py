import wavemap
from functools import partial
import numpy as np
from numpy import sin

SAMPLE_RATE = 44100
DURATION = 5
NSAMPLES = SAMPLE_RATE * DURATION
F_BEGIN = 200
F_END = 400
SCALE = 0.5
DTYPE = np.float64
RATIO = F_END / F_BEGIN
HALF_RATIO = 1 + (RATIO - 1) / 2

# The number of cycles at 1 hertz for the duration
CYCLES = 2 * np.pi * DURATION


def write(a, filename):
    wavemap.copy_to(a * SCALE, filename)


linspace = partial(np.linspace, endpoint=False, dtype=DTYPE, num=NSAMPLES)
geomspace = partial(np.geomspace, endpoint=False, dtype=DTYPE, num=NSAMPLES)

begin = linspace(0, F_BEGIN * CYCLES)
end = linspace(0, F_END * CYCLES)

write(sin(begin), 'begin.wav')
write(sin(end), 'end.wav')
write(sin(begin * linspace(1, RATIO)), 'bad-linear.wav')
write(sin(begin * linspace(1, HALF_RATIO)), 'linear.wav')
write(sin(begin * geomspace(1, RATIO)), 'bad-geom1.wav')
write(sin(begin * geomspace(1, HALF_RATIO)), 'bad-geom2.wav')
write(sin(begin * geomspace(1, np.sqrt(RATIO))), 'geom.wav')

# Why is the last one apparently correct?
