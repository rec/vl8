from ..grains import Grains
import itertools
import numpy as np


def stripe(samples, dtype, size, overlap, fader):
    grains = [Grains(s, size, overlap, fader) for s in samples]
    stride = grains[0].stride

    length = sum(s.shape[-1] for s in samples) + size
    buffer = np.zeros((2, length), dtype=dtype)

    time = 0
    for grain in itertools.izip_longest(*(iter(g) for g in grains)):
        for g in grain:
            if grain is not None:
                buffer[:, time : time + size] += grain
                time += stride

    return buffer
