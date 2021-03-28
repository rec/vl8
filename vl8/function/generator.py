from ..util import duration, ratio
from dataclasses import dataclass
from typing import Union
import numpy as np

DEFAULT_SAMPLE_RATE = 44100
DEFAULT_NCHANNELS = 2


@dataclass
class Generator:
    duration: ratio.Numeric = 0
    nchannels: int = DEFAULT_NCHANNELS
    sample_rate: int = DEFAULT_SAMPLE_RATE
    dtype: Union[np.dtype, str] = np.float32

    @property
    def sample_duration(self):
        return duration.to_samples(self.duration, self.sample_rate)

    def _make(self):
        shape = self.nchannels, self.sample_duration
        return self._maker(shape=shape, dtype=self.dtype)

    _maker = np.zeros

    def __call__(self):
        pass
