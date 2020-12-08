from dataclasses import dataclass
import numpy as np

GRAIN_SIZE = 1024


@dataclass
class Grains:
    data: np.ndarray
    size: int = GRAIN_SIZE
    overlap: float = 1.0
    dtype: np.dtype = np.float32

    def __post_init__(self):
        assert 0 <= self.overlap <= 1
        self.fade = round(self.overlap * self.size / 2)
        self.fade_in = np.linspace(
            0, 1, self.fade, endpoint=True, dtype=self.dtype
        )
        self.fade_out = np.flip(self.fade_in)

    def chunk(self, i):
        begin = i * (self.size - self.fade)
        c = self.data[:, begin : begin + self.size]
        missing = self.size - c.shape[1]
        if missing > 0:
            c = np.c_[c, np.zeros((2, missing), dtype=self.dtype)]

        return c

    def add_to(self, i, target):
        c = self.chunk(i)
        f = self.fade

        target[:, :f] += c[:, :f] * self.fade_in
        target[:, f : self.size - f] += c[:, f:-f]
        target[:, self.size - f : self.size] += c[:, -f:]
