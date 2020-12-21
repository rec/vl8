# from fractions import Fraction
from ..grain import Grain
import itertools
import numpy as np


def stripe(samples, dtype, grain):
    lengths = [max(s.shape) for s in samples]

    ml = max(lengths)
    # grain_count = overlap = variation = seed = size = 0

    def new_grain(sample):
        size = sample.size * ml / max(sample.shape)
        gr = dict(Grain(**vars(grain)))
        # TODO: overlap needs to be an absolute number
        # because here we have different-sized grains!
        # size = math.ceil( / grain_count)
        # Grains(size, overlap, variation, seed)

        return size, gr

    grains = [new_grain(s) for s in samples]
    size = stride = 0

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
