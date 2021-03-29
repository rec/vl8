# from fractions import Fraction

# from vl8.util import ratio
from vl8.dsp import curve_cache
from vl8.function.periodic import Periodic
import math
import numpy as np

# from typing import Optional


class Waveform(Periodic):
    curve: curve_cache.Curve = None
    # This is hard
    # duty_cycle: Optional[ratio.Number] = None

    @property
    def nperiods(self):
        return self.actual_duration / self.period

    def _base_curve(self):
        o = -2 * self.phase
        curve = curve_cache(self.curve, self.dtype)
        duration = math.ceil(self.sample_duration)
        c = curve(o, o + 2 * self.nperiods, duration)
        return np.row_stack([c] * self.nchannels)

    def _base_curve2(self):
        # Return a signal between -1 and 1
        p = self.phase * self.period
        print(p)

        arr = self()
        arr %= 2
        arr -= 1
        return arr

        o = -2 * self.phase
        curve = curve_cache(self.curve, self.dtype)
        duration = math.ceil(self.sample_duration)
        c = curve(o, o + 2 * self.nperiods, duration)
        return np.row_stack([c] * self.nchannels)


class Sawtooth(Waveform):
    def __call__(self):
        arr = self._base_curve()
        arr %= 2
        arr -= 1
        return arr


class Sine(Waveform):
    def __call__(self):
        arr = self._base_curve()
        arr *= np.pi
        np.sin(arr, out=arr)
        return arr


# Square
# Triangle
# Duty cycle
