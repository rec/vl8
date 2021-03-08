from ..grain import Grain
from dataclasses import dataclass
from fractions import Fraction
import copy
import itertools
import numpy as np

MIN_STRIPE_SIZE = 10


def stripe(samples, dtype, grain, rand):
    ms = Fraction(max(MIN_STRIPE_SIZE, *(max(s.shape) for s in samples)))

    grains = []
    for sample in samples:
        size = max(sample.shape)
        ratio = ms / size
        assert ratio >= 1, f'{ratio} < 1'
        gr = copy.copy(grain)
        gr.size *= ratio
        grains.append(list(gr.sizes(size, rand)))

    length = sum(s.shape[-1] for s in samples) + size
    buffer = np.zeros((2, length), dtype=dtype)

    time = 0
    # There is no iter(g)!
    for grain in itertools.izip_longest(*(iter(g) for g in grains)):
        for g in grain:
            if g is not None:
                buffer[:, time : time + size] += g
                # time += stride

    return buffer


@dataclass
class Stripe:
    grains: Grain
