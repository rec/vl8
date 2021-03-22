from . import curve_cache
from ..util import ratio
from .grain import Grain
from .rand import Rand
from dataclasses import dataclass
from typing import Optional

SIZE = 1 / 32


@dataclass
class TimeGrain:
    """Grains from within a larger sample, with optional overlaps and
       optional variation"""

    size: float = SIZE
    """Size of each grain, in seconds.  Must be non-negative"""

    overlap: ratio.Ratio = 1 / 2
    """Overlap ratio between grains, between 0 and 1 inclusive"""

    rand: Optional[Rand] = None
    curve: Optional[curve_cache.Curve] = None

    def __post_init__(self):
        if self.overlap < 0:
            raise ValueError('overlap cannot be negative')

    def to_grain(self, sample_rate) -> Grain:
        size = ratio.to_fraction(self.size * sample_rate)
        return Grain(**dict(self.asdict(), size=size))
