from ..dsp.grains import Grains
import numpy as np


def sorter(sample, dtype, grain):
    buffer = np.zeros((2, sample.data.shape[-1] + grain.size), dtype=dtype)
    assert Grains
    return buffer
