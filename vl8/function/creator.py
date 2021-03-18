from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class Creator:
    dtype: Optional[np.dtype] = None

    def _channels(self, src):
        return max(s.shape[0] for s in src)

    def _duration(self, src):
        return max(s.shape[1] for s in src)

    def _call(self, x):
        return x

    _make = np.zeros

    def __call__(self, *src):
        shape = self._channels(src), self._duration(src)
        dtype = self.dtype or src[0].dtype
        arr = self._make(shape=shape, dtype=dtype)
        return self._call(arr, *src)
