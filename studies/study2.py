import wavemap
from functools import partial
import numpy as np
from numpy import sin

SAMPLE_RATE = 44100
SCALE = 0.5
DTYPE = np.float64

linspace = partial(np.linspace, endpoint=False, dtype=DTYPE)
geomspace = partial(np.geomspace, endpoint=False, dtype=DTYPE)


def write(a, filename):
    wavemap.copy_to(a * SCALE, filename)


# Goal: a classic descending Shephard tone
# N parts
# Mono
# Fade in
# Fade out
# A way to slice and combine samples


def ramp(begin, end, duration, fade_in, fade_out):
    nsamples = round(duration * SAMPLE_RATE)
    cycles = duration * 2 * np.pi
