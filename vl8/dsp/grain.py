from . import curve_cache
from ..util import ratio
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

    overlap: ratio.Ratio = 1 / 2
    """Overlap ratio between grains, between 0 and 1 inclusive"""

    rand: Optional[Rand] = None
    curve: Optional[curve_cache.Curve] = None

    def __post_init__(self):
        assert self.overlap >= 0
        self._curves = curve_cache(self.curve, 'float32')
        fs = self._fade_size = round(self.overlap * self.size)
        self._fade_in = fs and self._curves(0, 1, fs)
        self._fade_out = fs and self._curves(1, 0, fs)

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
        sizes = self.sizes(data.shape[1])
        yield from (self.chunk(data, b, e) for b, e in sizes)

    def chunk(self, data, begin, end):
        chunk = data[:, begin:end]
        chunk = np.copy(chunk)

        if self._fade_size <= 0:
            return chunk

        def mul(x, y):
            # TODO: unsafe leaves the possibility of overs in a fixed-point
            # format.
            # print('BEFORE', x, y)
            np.multiply(x, y, out=x, casting='unsafe')
            # print('AFTER', x, y)

        duration = chunk.shape[1]
        if duration >= 2 * self._fade_size:
            # print('TWO')
            mul(chunk[:, : self._fade_size], self._fade_in)
            mul(chunk[:, -self._fade_size :], self._fade_out)
        else:
            # print('THREE')
            fs = duration // 2
            mul(chunk[:, :fs], self._fade_in[:fs])
            mul(chunk[:, fs:], self._fade_out[fs - duration :])

        return chunk
