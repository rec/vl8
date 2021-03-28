from vl8.dsp import curve_cache
from vl8.function.periodic import Periodic
import math


class Sawtooth(Periodic):
    curve: curve_cache.Curve = None

    def __call__(self):
        periods = self.sample_duration / self.period
        off = -2 * self.phase
        curve = curve_cache(self.curve, self.dtype)
        arr = curve(off, off + 2 * periods, math.ceil(self.sample_duration))
        arr %= 2
        arr -= 1
        return arr
