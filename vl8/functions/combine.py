import functools
import math
import numpy as np
import sys

"""

gap: None, a number of seconds or a list of seconds
if a gap is negative, it's a fade
"""


def combine(sources, dtype, curve=np.linspace, gap=0, pre=0, post=0):
    @functools.lru_cache()
    def fader(a, b, gap):
        return curve(a, b, gap, endpoint=True, dtype=dtype)

    if isinstance(gap, (list, tuple)):
        gaps = list(gap)
    else:
        gaps = [gap or 0]
    gaps *= math.ceil((len(sources)) / len(gaps))

    # Fix any fade gaps that are too long.
    for i, src in enumerate(sources):
        gi = gaps[i]
        gaps[i] = max(gaps[i], -src.shape[-1])
        if i:
            gaps[i] = max(gaps[i], -sources[i - 1].shape[-1])
        if gi != gaps[i]:
            print(f'fade {gi} was longer than the sample!', file=sys.stderr)

    gaps = [0] + gaps[: len(sources) - 1] + [0]
    duration = pre + sum(s.shape[-1] for s in sources) + sum(gaps) + post
    channels = max(s.shape[0] for s in sources)
    result = np.zeros((channels, duration), dtype=dtype)

    end = pre
    for i, src in enumerate(sources):
        g0, g1 = gaps[i : i + 2]
        begin = end + g0
        end = begin + src.shape[-1]

        b, e = begin, end
        if g0 < 0:  # Fade in
            fade = -g0
            result[:, b : b + fade] += fader(0, 1, fade) * src[:, :fade]
            b += fade

        if g1 < 0:  # Fade out
            fade = -g1
            result[:, e - fade : e] += fader(1, 0, fade) * src[:, -fade:]
            e -= fade

        result[:, b:e] += src[:, b - begin : e - end or None]

    return result


"""
# Should be elsewhere in a task

overlap: None or any floating point numbers, referenced to the longest item.

These next comments shoul

0 means: all start together
0.5 means: middles of all songs are at same time
1 means: all end together

Negative numbers and numbers bigger than one are possible!
"""
