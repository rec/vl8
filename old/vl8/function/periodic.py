from ..types import to_number, to_seconds, types
from .generator import Generator
from dataclasses import dataclass
from typing import Optional


@dataclass
class Periodic(Generator):
    cycles: Optional[int] = None
    phase: types.NumericSequence = 0
    period: Optional[types.Number] = None
    frequency: Optional[types.Number] = None

    @property
    def actual_duration(self):
        dur = super().actual_duration
        if self.cycles is None:
            return dur
        cycles = to_number(self.cycles) * self.period
        return min(dur, cycles) if dur else cycles

    def _get_period(self) -> types.Number:
        if self._period or not self._frequency:
            return self._period
        return 1 / self.frequency

    def _set_period(self, period: Optional[types.Numeric]):
        self._period = period and to_seconds(period, self.sample_rate)
        if period:
            self._frequency = None

    def _get_frequency(self) -> types.Number:
        if self._frequency or not self._period:
            return self._frequency
        return 1 / self.period

    def _set_frequency(self, f: Optional[types.Numeric]):
        self._frequency = f and to_number(f)
        if f:
            self._period = None

    def _get_phase(self) -> types.Number:
        return self._phase

    def _set_phase(self, phase: types.Numeric):
        self._phase = to_number(phase)


Periodic.frequency = property(Periodic._get_frequency, Periodic._set_frequency)
Periodic.period = property(Periodic._get_period, Periodic._set_period)
Periodic.phase = property(Periodic._get_phase, Periodic._set_phase)
