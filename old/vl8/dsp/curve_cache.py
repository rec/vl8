from ..function import importer
from typing import Callable, Union
import functools
import numpy as np
import xmod

Curve = Union[str, Callable, None]


def to_callable(curve: Curve):
    if callable(curve):
        return curve

    if curve is None:
        return np.linspace

    assert isinstance(curve, str)
    return importer(curve, 'numpy')


@functools.lru_cache()
def make(curve: Curve, dtype: np.dtype, endpoint=True):
    @functools.wraps(curve)
    @functools.lru_cache()
    def f(a, b, gap):
        return curve(a, b, gap, endpoint=endpoint, dtype=dtype)

    return f


@xmod
def curve_cache(curve: Curve, dtype: np.dtype):
    return make(to_callable(curve), dtype)
