from dataclasses import dataclass
import wavemap
from functools import partial
import numpy as np
# from numpy import sin

SAMPLE_RATE = 44100
SCALE = 0.5

linspace = partial(np.linspace, endpoint=False)
geomspace = partial(np.geomspace, endpoint=False)


def write(a, filename):
    wavemap.copy_to(a * SCALE, filename)


# Goal: a classic descending Shephard tone
# N parts
# Mono
# Fade in
# Fade out
# A way to slice and combine samples


def _samples(duration):
    return round(duration * SAMPLE_RATE)


@dataclass
class Ramp:
    f_begin: float
    f_end: float
    duration: float
    linear: bool = False

    def __call__(self):
        nsamples = _samples(self.duration)
        s = linspace(0, self.begin * self.duration * 2 * np.pi, nsamples)

        ratio = self.f_end / self.f_begin
        if self.linear:
            s *= linspace(1, 1 + (ratio - 1) / 2, nsamples)
        else:
            s *= geomspace(1, np.sqrt(ratio), nsamples)

        return np.sin(s, out=s)
