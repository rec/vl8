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

    def _base_curve(self, phase):
        # Return a signal between -1 and 1
        begin = -2 * phase
        end = begin + self.nperiods
        steps = math.ceil(self.sample_duration)
        arr = np.linspace(begin, end, steps, dtype=self.dtype)
        arr %= 2
        arr -= 1
        return np.row_stack([arr] * self.nchannels)


class Sawtooth(Waveform):
    def __call__(self):
        arr = self._base_curve(self.phase)
        arr %= 2
        arr -= 1
        return arr


class Sine(Waveform):
    def __call__(self):
        arr = self._base_curve(self.phase)
        arr *= np.pi
        np.sin(arr, out=arr)
        return arr


# Square
# Triangle
# Duty cycle
