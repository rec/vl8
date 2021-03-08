import numpy as np


def precis(sample, dtype, size):
    buffer = np.zeros((2, size), dtype=dtype)
    for i in range(0, sample.shape[-1], size):
        region = sample.data[:, i : i + size]
        to_cut = size - region.shape[-1]
        if to_cut > 0:
            buffer[:, :-to_cut] += region
        else:
            buffer += region

    return buffer
