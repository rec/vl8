from . import DEFAULT_SAMPLE_RATE
import functools
import numpy as np
import pyrubberband as rb


def _rubber(f):
    @functools.wraps(f)
    def wrapped(data, value, sample_rate=DEFAULT_SAMPLE_RATE, **kwargs):
        if data.dtype == np.int8:
            data = data.astype(np.int16)

        data = np.transpose(data)
        data = f(data, sample_rate, value, kwargs)
        return np.transpose(data)

    return wrapped


time_stretch = _rubber(rb.time_stretch)
pitch_shift = _rubber(rb.pitch_shift)
