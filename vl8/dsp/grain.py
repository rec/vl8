from . import curve_cache
from . import fade
from ..types import duration, to_fraction, types
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
    nsamples: Fraction = SIZE
    """Size of each grain, in fractional samples.  Must be non-negative"""

    overlap: Optional[Fraction] = None
    """Overlap, in fractional samples.  None means use 1/2 of SIZE"""

    def __post_init__(self):
        if self.overlap is None:
            self.overlap = Fraction(self.nsamples, 2)
        else:
            assert (
                0 <= self.overlap <= self.nsamples
            ), f'{float(self.overlap)} >= {float(self.nsamples)}'

    @property
    def stride(self) -> Fraction:
        return self.nsamples - self.overlap

    def sizes(self, size: int) -> Iterator[Tuple[int]]:
        if self.nsamples < 0:
            return
        begin = 0
        while begin < size:
            end = begin + self.nsamples
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

    duration: types.NonInteger = SIZE
    """Size of each grain, in seconds.  Must be non-negative"""

    overlap: types.Numeric = 1 / 2
    """Overlap ratio between grains, between 0 and 1 inclusive"""

    def __post_init__(self):
        if not (0 <= self.overlap <= 1):
            raise ValueError(f'Bad overlap {self.overlap}')

    @property
    def stride(self) -> Fraction:
        return self.size * (1 - self.overlap)

    def to_samples(self, sample_rate) -> GrainSamples:
        nsamples = duration.to_samples(self.duration, sample_rate)
        overlap = nsamples * to_fraction(self.overlap)
        return GrainSamples(
            nsamples=nsamples,
            overlap=overlap,
            rand=self.rand,
            curve=self.curve,
        )


def make_grain(**kwargs: dict):
    if 'nsamples' in kwargs and 'duration' not in kwargs:
        return GrainSamples(**kwargs)
    if 'duration' in kwargs:
        return Grain(**kwargs)
    raise ValueError('Exactly one of nsamples and duration must be set')


GrainType = Union[GrainSamples, Grain, dict]
