from vl8.dsp import curve_cache
from vl8.function.periodic import Periodic
import math
import numpy as np


class Sawtooth(Periodic):
    curve: curve_cache.Curve = None

    def __call__(self):
        arr = self._base_curve()
        arr %= 2
        arr -= 1
        return arr

    def _base_curve(self):
        ncycles = self.actual_duration / self.period
        off = -2 * self.phase
        curve = curve_cache(self.curve, self.dtype)
        c = curve(off, off + 2 * ncycles, math.ceil(self.sample_duration))
        return np.row_stack([c] * self.nchannels)


class Sine(Sawtooth):
    def __call__(self):
        arr = self._base_curve()
        arr *= np.pi
        np.sin(arr, out=arr)
        return arr
