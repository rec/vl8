import numpy as np


def shuffler(data, dtype, grain, shuffle):
    buffer = np.zeros((2, data.shape[-1] + grain.size), dtype=dtype)
    grains = list(grain.grains(data))

    return buffer, grains
