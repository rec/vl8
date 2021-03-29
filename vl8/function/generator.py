from ..types import duration, ratio
from dataclasses import dataclass
from typing import Union
import math
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
    def actual_duration(self):
        return duration.to_seconds(self.duration, self.sample_rate)

    @property
    def sample_duration(self):
        return duration.to_samples(self.actual_duration, self.sample_rate)

    @property
    def shape(self):
        return self.nchannels, math.ceil(self.sample_duration)

    def __call__(self):
        return self._make(shape=self.shape, dtype=self.dtype)
