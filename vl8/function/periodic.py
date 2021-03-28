from ..util import duration, ratio
from .generator import Generator
from dataclasses import dataclass
from typing import Optional


@dataclass
class Periodic(Generator):
    cycles: Optional[int] = None
    phase: ratio.Numeric = 0
    period: Optional[ratio.Number] = None
    frequency: Optional[ratio.Number] = None

    def _get_period(self) -> ratio.Number:
        if self._period or not self._frequency:
            return self._period
        return 1 / self.frequency

    def _set_period(self, period: Optional[ratio.Numeric]):
        self._period = period and duration.to_seconds(period, self.sample_rate)
        if period:
            self._frequency = None

    def _get_frequency(self) -> ratio.Number:
        if self._frequency or not self._period:
            return self._frequency
        return 1 / self.period

    def _set_frequency(self, f: Optional[ratio.Numeric]):
        self._frequency = f and ratio.to_number(f)
        if f:
            self._period = None

    def _actual_duration(self):
        dur = self.duration
        dur = dur and duration.to_seconds(dur, self.sample_rate)
        if self.cycles is None:
            return dur
        cycles = ratio.to_number(self.cycles) * self.period
        return min(dur, cycles) if dur else cycles


Periodic.period = property(Periodic._get_period, Periodic._set_period)
Periodic.frequency = property(Periodic._get_frequency, Periodic._set_frequency)
Periodic.actual_duration = property(Periodic._actual_duration)
