from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class Creator:
    dtype: Optional[np.dtype] = None

    def _prepare(self, src):
        # Return the duration of the result, in samples
        return max(s.nsamples for s in src)

    def _call(self, x):
        pass

    _make = np.zeros

    def __call__(self, *src):
        nchannels = max(s.nchannels for s in src)
        duration = self._prepare(src)
        shape = nchannels, duration
        dtype = self.dtype or src[0].dtype
        arr = self._make(shape=shape, dtype=dtype)
        res = self._call(arr, *src)
        return arr if res is None else res
