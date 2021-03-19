from .rand import Rand
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterator, Optional, Tuple
import numpy as np

SIZE = Fraction(1024)


@dataclass
class Grain:
    """Grains from within a larger sample, with optional overlaps and
       optional variation"""

    size: Fraction = SIZE
    """Size of each grain, in fractional samples.  Must be non-negative"""

    overlap: Fraction = Fraction(1, 2)
    """Overlap ratio between grains, between 0 and 1 inclusive"""

    rand: Optional[Rand] = None

    @property
    def stride(self) -> Fraction:
        assert 0 <= self.overlap <= 1
        return self.size * (1 - self.overlap)

    def sizes(self, size: int) -> Iterator[Tuple[int]]:
        begin = 0
        while begin < size:
            end = begin + self.size
            if self.rand:
                end += self.rand()
            yield round(begin), round(min(size, end))
            begin = end - self.overlap * self.size

    def chunks(self, data: np.ndarray) -> Iterator[np.ndarray]:
        for begin, end in self.sizes(max(data.shape)):
            yield data[:, begin:end]
