import math
import numpy as np
import sys

"""

gap: None, a number of seconds or a list of seconds
if a gap is negative, it's a fade

overlap: None or any floating point numbers, referenced to the longest item.

0 means: all start together
0.5 means: middles of all songs are at same time
1 means: all end together

Negative numbers and numbers bigger than one are possible!

"""


def combine(samples, dtype, gap=0, pre=0, post=0):
    if isinstance(gap, (list, tuple)):
        gaps = list(gap)
    else:
        gaps = [gap or 0]
    gaps *= math.ceil((len(samples)) / len(gaps))

    # Fix any fade gaps that are too long.
    for i, sample in enumerate(samples):
        gi = gaps[i]
        gaps[i] = max(gaps[i], -sample.shape[1])
        if i:
            gaps[i] = max(gaps[i], -samples[i - 1].shape[1])
        if gi != gaps[i]:
            print('sample was too short for gap', file=sys.stderr)

    duration = pre + sum(s.shape[-1] for s in samples) + sum(gaps) + post
    channels = max(s.shape[0] for s in samples)
    result = np.zeros((channels, duration), dtype=dtype)

    end = pre
    for sample, gap in zip(samples, [0] + gaps):
        begin = end + gap
        end = begin + sample.shape[-1]

        if gap >= 0:
            result[:, begin:end] = sample
            continue

        intro = sample[:, :-gap]
        remains = sample[:, -gap:]

        fade_end = begin - gap
        fade_in = np.linspace(0, 1, -gap, endpoint=True, dtype=dtype)
        fade_out = fade_in[::-1]

        result[:, begin:fade_end] *= fade_out
        result[:, begin:fade_end] += fade_in * intro

        result[:, fade_end : fade_end + remains.shape[1]] = remains

    return result
