from . import curve_cache
from . import fade
from ..util import ratio
from .rand import Rand
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterator, Optional, Tuple
import numpy as np

SIZE = Fraction(1024)


@dataclass
class _GrainBase:
    overlap: ratio.Numeric = 1 / 2
    """Overlap ratio between grains, between 0 and 1 inclusive"""

    rand: Optional[Rand] = None
    curve: Optional[curve_cache.Curve] = None

    def __post_init__(self):
        if self.overlap < 0:
            raise ValueError('overlap cannot be negative')

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
        for begin, end in self.sizes(data.shape[1]):
            chunk = np.copy(data[:, begin:end])
            fade(chunk, self._fade_in, self._fade_out)
            yield chunk


@dataclass
class Grain(_GrainBase):
    """Grains from within a larger sample, with optional overlaps and
       optional variation"""

    size: Fraction = SIZE
    """Size of each grain, in fractional samples.  Must be non-negative"""

    def __post_init__(self):
        assert self.overlap >= 0
        self._curves = curve_cache(self.curve, 'float32')
        fs = self._fade_size = round(self.overlap * self.size)
        self._fade_in = self._curves(0, 1, fs) if fs else []
        self._fade_out = self._curves(1, 0, fs) if fs else []


@dataclass
class TimeGrain(_GrainBase):
    """Grains from within a larger sample, with optional overlaps and
       optional variation"""

    size: float = SIZE
    """Size of each grain, in seconds.  Must be non-negative"""

    def to_grain(self, sample_rate) -> Grain:
        size = ratio.to_fraction(self.size * sample_rate)
        return Grain(**dict(self.asdict(), size=size))
