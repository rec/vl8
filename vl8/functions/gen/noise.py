from dataclasses import dataclass
from typing import Optional
from vl8.dsp.rand import Rand
from vl8.function.generator import Generator
import numpy as np


@dataclass
class Noise(Generator):
    rand: Optional[Rand] = None
    normalize: bool = True

    def __call__(self):
        arr = self.rand(size=self.shape)
        self.normalize and _normalize(arr)
        return arr


def _normalize(arr):
    lo, hi = np.amin(arr), np.amax(arr)
    if lo != hi:
        m = 2 / (hi - lo)
        a = (hi + lo) / (hi - lo)
        arr *= m
        arr -= a
