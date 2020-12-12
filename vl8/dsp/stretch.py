from . import DEFAULT_SAMPLE_RATE
import numpy as np
import pyrubberband as rb


def time_stretch(data, ratio, sample_rate=DEFAULT_SAMPLE_RATE, **kwargs):
    d = np.transpose(data)
    s = rb.time_stretch(d, sample_rate, ratio * sample_rate, kwargs)
    return np.transpose(s)


def pitch_shift(data, steps, sample_rate=DEFAULT_SAMPLE_RATE, **kwargs):
    d = np.transpose(data)
    s = rb.pitch_shift(d, sample_rate, steps, kwargs)
    return np.transpose(s)
