from . import DEFAULT_SAMPLE_RATE
from wavemap import wavemap
import numpy as np


def read(file, *args, **kwargs):
    data = wavemap(file, *args, **kwargs)
    return data, data.sample_rate


def write(
    filename: str,
    data: np.ndarray,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    **kwds,
):
    return wavemap.copy_to(data, filename, sample_rate, **kwds)
