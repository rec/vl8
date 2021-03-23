from . import curve_cache
from . import fade
from ..util import ratio
from .rand import Rand
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterator, Optional, Tuple, Union
import numpy as np

SIZE = Fraction(1024)


@dataclass
class _Grain:
    """Grains from within a larger sample, with optional overlaps and
       optional variation"""

    rand: Optional[Rand] = None
    curve: Optional[curve_cache.Curve] = None


@dataclass
class GrainSamples(_Grain):
    sample_count: Fraction = SIZE
    """Size of each grain, in fractional samples.  Must be non-negative"""

    overlap: Optional[Fraction] = None
    """Overlap, in fractional samples.  None means use 1/2 of SIZE"""

    @property
    def stride(self) -> Fraction:
        return self.sample_count - self.overlap

    def __post_init__(self):
        if self.overlap is None:
            self.overlap = Fraction(self.sample_count, 2)
        else:
            assert 0 <= self.overlap <= self.sample_count

    def sizes(self, size: int) -> Iterator[Tuple[int]]:
        if self.sample_count < 0:
            return
        begin = 0
        while begin < size:
            end = begin + self.sample_count
            if self.rand:
                end += self.rand()
            yield round(begin), round(min(size, end))
            b, begin = begin, end - self.overlap
            if begin <= b:
                raise ValueError('Made no progress')

    def chunks(self, data: np.ndarray) -> Iterator[np.ndarray]:
        function = curve_cache.to_callable(self.curve)
        o = round(self.overlap)

        if o > 0:
            fade_in = function(0, 1, o, endpoint=True, dtype=np.float32)
            fade_out = 1 - fade_in
        else:
            fade_in = fade_out = []

        for begin, end in self.sizes(data.shape[1]):
            chunk = np.copy(data[:, begin:end])
            fade(chunk, fade_in, fade_out)
            yield chunk


@dataclass
class Grain(_Grain):
    """A description of a grain with a duration in seconds"""

    duration: ratio.NonInteger = SIZE
    """Size of each grain, in seconds.  Must be non-negative"""

    overlap: ratio.Numeric = 1 / 2
    """Overlap ratio between grains, between 0 and 1 inclusive"""

    def __post_init__(self):
        if not (0 <= self.overlap <= 1):
            raise ValueError(f'Bad overlap {self.overlap}')

    @property
    def stride(self) -> Fraction:
        return self.size * (1 - self.overlap)

    def to_samples(self, sample_rate) -> GrainSamples:
        sample_count = sample_rate * ratio.to_fraction(self.duration)
        overlap = sample_count * ratio.to_fraction(self.overlap)
        return GrainSamples(
            sample_count=sample_count,
            overlap=overlap,
            rand=self.rand,
            curve=self.curve,
        )


def make_grain(**kwargs: dict):
    if 'sample_count' in kwargs and 'duration' not in kwargs:
        return GrainSamples(**kwargs)
    if 'duration' in kwargs:
        return Grain(**kwargs)
    raise ValueError('Exactly one of sample_count and duration must be set')


GrainType = Union[GrainSamples, Grain, dict]
