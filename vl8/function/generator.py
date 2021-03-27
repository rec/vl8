from ..util import duration
from dataclasses import dataclass
from typing import Union
import numpy as np

DEFAULT_SAMPLE_RATE = 44100
DEFAULT_NCHANNELS = 2


@dataclass
class Generator:
    duration: duration.Numeric
    nchannels: int = DEFAULT_NCHANNELS
    sample_rate: int = DEFAULT_SAMPLE_RATE
    dtype: Union[np.dtype, str] = np.float32

    def _prepare(self):
        # Return the duration of the result, in samples
        return duration.to_samples(self.duration, self.sample_rate)

    def _call(self, x):
        pass

    _make = np.zeros

    def __call__(self):
        duration = self._prepare()
        arr = self._make(shape=(self.channels, duration), dtype=self.dtype)
        res = self._call(arr)
        return arr if res is None else res
