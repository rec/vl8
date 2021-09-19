import numpy as np


def sorter(data, dtype, grain, sorter):
    buffer = np.zeros((2, data.shape[-1] + grain.size), dtype=dtype)

    return buffer
