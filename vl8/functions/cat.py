from ..dsp import curve_cache
from ..dsp.data import Data
from ..util import fix_gaps
import numpy as np


def target(src, f_channel=max, f_duration=max, dtype=None, f_make=np.zeros):
    channels, durations = zip(*(s.shape for s in src))
    shape = f_channel(channels), f_duration(durations)
    return f_make(shape, dtype or src[0].dtype)


def cat(*src, dtype=None, curve=np.linspace, gap=0, pre=0, post=0):
    """
    gap: None, a number of seconds or a list of seconds
    if a gap is negative, it's a fade
    """

    gaps = []

    def duration(durations):
        gaps[:] = fix_gaps(durations, gap, pre, post, src[0].sample_rate)
        return sum(durations) + sum(gaps)

    arr = target(src, f_duration=duration, dtype=dtype)
    fader = curve_cache(curve, arr.dtype)

    begin = end = 0
    for i, s in enumerate(src):
        begin = end + gaps[i]
        end = begin + s.shape[-1]
        fade_in, fade_out = -gaps[i], -gaps[i + 1]

        b, e = begin, end
        if fade_in > 0:
            delta = fader(0, 1, fade_in) * s[:, :fade_in]
            arr[:, b : b + fade_in] += delta
            b += fade_in

        if fade_out > 0:
            delta = fader(1, 0, fade_out) * s[:, -fade_out:]
            arr[:, e - fade_out : e] += delta
            e -= fade_out

        arr[:, b:e] += s[:, b - begin : e - end or None]

    return Data(arr, src[0].sample_rate)


"""
# Should be elsewhere in a task

overlap: None or any floating point numbers, referenced to the longest item.

These next comments shoul

0 means: all start together
0.5 means: middles of all songs are at same time
1 means: all end together

Negative numbers and numbers bigger than one are possible!
"""
