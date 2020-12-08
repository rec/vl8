from . import fader
from dataclasses import dataclass
import math
import numpy as np

GRAIN_SIZE = 1024
OVERLAP = 0.5


@dataclass
class Grains:
    data: np.ndarray
    size: int = GRAIN_SIZE
    overlap: float = OVERLAP
    fader: object = None
    dtype: np.dtype = np.float32

    def __post_init__(self):
        o = OVERLAP if self.overlap is None else self.overlap
        fade = round(o * self.size / 2)
        self.stride = self.size - fade
        if self.fader is None:
            self.fader = fader.Fader(fade, dtype=self.dtype)

    def __len__(self):
        return math.ceil(self.data.shape[-1] / self.stride)

    def __getitem__(self, i):
        begin = i * self.stride
        g = self.data[:, begin : begin + self.size]
        missing = self.size - g.shape[-1]
        if missing >= 0:
            g = np.c_[g, np.zeros((2, missing), dtype=self.dtype)]
        return g
