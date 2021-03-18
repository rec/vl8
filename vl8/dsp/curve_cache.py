from ..function import importer
import functools
import numpy as np
import xmod


@xmod
def curve_cache(curve, dtype):
    if not callable(curve):
        curve = importer(curve or 'numpy.linspace', 'numpy')
    return _make_curve(curve, np.dtype(dtype))


@functools.lru_cache()
def _make_curve(curve, dtype):
    @functools.lru_cache()
    def f(a, b, gap):
        return curve(a, b, gap, endpoint=True, dtype=dtype)

    return f
