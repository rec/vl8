from . import curve_cache
from .grain import Grain
from .rand import Rand
from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Tuple

SIZE = Fraction(1024)


@dataclass
class TimeGrain:
    """Grains from within a larger sample, with optional overlaps and
       optional variation"""

    size: float = 1 / 32
    """Size of each grain, in seconds.  Must be non-negative"""

    overlap: Overlap = Fraction(1, 2)
    """Overlap ratio between grains, between 0 and 1 inclusive"""

    rand: Optional[Rand] = None
    curve: Optional[curve_cache.Curve] = None

    def __post_init__(self):
        assert self.overlap >= 0
