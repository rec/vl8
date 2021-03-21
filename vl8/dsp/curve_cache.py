from ..function import importer
from typing import Callable, Union
import functools
import numpy as np
import xmod

Curve = Union[str, Callable, None]


@functools.lru_cache()
def make(curve: Curve, dtype: np.dtype):
    @functools.lru_cache()
    def f(a, b, gap):
        return curve(a, b, gap, endpoint=True, dtype=dtype)

    return f


@xmod
def curve_cache(curve: Curve, dtype: np.dtype):
    curve = curve or np.linspace
    if not callable(curve):
        curve = importer(curve, 'numpy')
    return make(curve, dtype)
