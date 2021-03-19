from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class Creator:
    dtype: Optional[np.dtype] = None

    def _prepare(self, src):
        # Return the duration of the result, in samples
        return max(s.shape[1] for s in src)

    def _call(self, x):
        return x

    _make = np.zeros

    def __call__(self, *src):
        channels = max(s.shape[0] for s in src)
        duration = self._prepare(src)
        shape = channels, duration
        dtype = self.dtype or src[0].dtype
        arr = self._make(shape=shape, dtype=dtype)
        self._call(arr, *src)
        return arr
