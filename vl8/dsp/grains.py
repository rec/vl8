from .fader import Fader
from dataclasses import dataclass
import math
import numpy as np

GRAIN_SIZE = 1024
OVERLAP = 0.5


class Grain:
    def __init__(self, size=GRAIN_SIZE, overlap=OVERLAP):
        self.size = size
        self.overlap = overlap
        self.fade = round(self.overlap * self.size / 2)
        self.stride = self.size - self.fade
        self.fader = Fader(self.fade)


@dataclass
class Grains:
    data: np.ndarray
    grain: Grain

    def __len__(self):
        return math.ceil(self.data.shape[-1] / self.grain.stride)

    def __getitem__(self, i):
        begin = i * self.grain.stride
        g = self.data[:, begin : begin + self.grain.size]
        missing = self.grain.size - g.shape[-1]
        if missing >= 0:
            zeros = np.zeros((2, missing), dtype=self.data.dtype)
            g = np.c_[g, zeros]
        return g
