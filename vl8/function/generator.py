from ..types import to_samples, to_seconds, types
from dataclasses import dataclass
from typing import Optional, Union
import math
import numpy as np

DEFAULT_SAMPLE_RATE = 44100
DEFAULT_NCHANNELS = 2
DEFAULT_DURATION = 10


@dataclass
class Generator:
    duration: Optional[types.Numeric] = None
    nchannels: int = DEFAULT_NCHANNELS
    sample_rate: int = DEFAULT_SAMPLE_RATE
    dtype: Union[np.dtype, str] = np.float32

    @property
    def actual_duration(self):
        d = DEFAULT_DURATION if self.duration is None else self.duration
        return to_seconds(d, self.sample_rate)

    @property
    def sample_duration(self):
        return to_samples(self.actual_duration, self.sample_rate)

    @property
    def shape(self):
        return self.nchannels, math.ceil(self.sample_duration)

    def __call__(self):
        return self._make(shape=self.shape, dtype=self.dtype)
