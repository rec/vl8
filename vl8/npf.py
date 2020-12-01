import functools
import numpy as np
import xmod


class Npf:
    def __getattr__(self, name):
        value = getattr(np, name)
        if name in STEREO:
            return _stereo(value)

        if name in FLOAT:
            return functools.partial(value, dtype=np.float32)

        return value


def _stereo(f):
    @functools.wraps(f)
    def wrapped(length, channels=2, *args, **kwargs):
        return f(shape=(channels, length), *args, dtype=np.float32, **kwargs)

    return wrapped


STEREO = {'empty', 'ones', 'zeros', 'full'}
FLOAT = {
    'arange',
    'linspace',
    'logspace',
    'geomspace',
    'meshgrid',
    'mgrid',
    'ogrid',
}

__all__ = dir(np)

xmod(Npf(), full=True)
