from ..grains import Grains
import itertools
import math
import numpy as np


def stripe(samples, dtype, grain):
    lengths = [s.shape[-1] for s in samples]
    min_l, max_l = min(lengths), max(lengths)
    print(min_l, max_l)

    grain_count = overlap = variation = seed = size = 0

    def gr(sample):
        # TODO: overlap needs to be an absolute number
        # because here we have different-sized grains!
        size = math.ceil(sample.shape[-1] / grain_count)
        return Grains(size, overlap, variation, seed)

    grains = [gr(s) for s in samples]
    stride = grains[0].stride  # Wrong

    length = sum(s.shape[-1] for s in samples) + size
    buffer = np.zeros((2, length), dtype=dtype)

    time = 0
    # There is no iter(g)!
    for grain in itertools.izip_longest(*(iter(g) for g in grains)):
        for g in grain:
            if g is not None:
                buffer[:, time : time + size] += g
                time += stride

    return buffer
