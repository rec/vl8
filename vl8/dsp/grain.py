from .rand import Rand
from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

SIZE = Fraction(1024)


@dataclass
class Grain:
    """Grains from within a larger sample, with optional overlaps and
       optional variation"""

    size: Fraction = SIZE
    """Size of each grain, in fractional samples.  Must be non-negative"""

    overlap: Fraction = SIZE / 2
    """Overlap between grains, in fractional samples.  Must be non-negative."""

    rand: Optional[Rand] = None

    @property
    def stride(self):
        return self.size - self.overlap

    def sizes(self, size):
        begin = 0
        while begin < size:
            end = begin + self.size + (self.rand() if self.rand else 0)
            yield round(begin), round(min(size, end))
            begin = end - self.overlap

    def grains(self, data):
        for begin, end in self.sizes(max(data.shape)):
            yield data[:, begin:end]
