from . import io
from dataclasses import dataclass
import numpy as np

DEFAULT_SAMPLE_RATE = 44100


@dataclass
class Sample:
    data: np.ndarray
    sample_rate: int = DEFAULT_SAMPLE_RATE

    def __post_init__(self):
        length, *rest = self.data.shape
        if not rest:
            self.data = self.data.reshape((1, length))

    @classmethod
    def read(cls, filename):
        return cls(*io.read(filename))

    def write(self, out_f, *args, **kwargs):
        return io.write(self.data, out_f, self.sample_rate, *args, **kwargs)
