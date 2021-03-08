from dataclasses import dataclass
from typing import Callable, Union, List
import functools
import math
import numpy as np
import sys


def cat(sources, dtype, curve=np.linspace, gap=0, pre=0, post=0):
    return Cat()


@dataclass
class Cat:
    curve: Callable = np.linspace

    """
    gap: a number of seconds or a list of seconds
    if a gap is negative, it's an overlap with a fade
    """
    gaps: Union[float, List[float]] = 0
    pre: float = 0
    post: float = 0
    curve: Callable = np.linspace

    def __call__(self, sources, target, dtype):
        @functools.lru_cache()
        def fader(a, b, gap):
            return self.curve(a, b, gap, endpoint=True, dtype=dtype)

        if isinstance(self.gap, (list, tuple)):
            gaps = list(self.gap)
        else:
            gaps = [self.gap or 0]
        gaps *= math.ceil((len(sources)) / len(gaps))

        # Fix any fade gaps that are too long.
        for i, src in enumerate(sources):
            gi = gaps[i]
            gaps[i] = max(gaps[i], -src.shape[-1])
            if i:
                gaps[i] = max(gaps[i], -sources[i - 1].shape[-1])
            if gi != gaps[i]:
                print(
                    f'fade {gi} was longer than the sample!', file=sys.stderr
                )

        gaps = [0] + gaps[: len(sources) - 1] + [0]
        duration = (
            self.pre
            + sum(s.shape[-1] for s in sources)
            + sum(gaps)
            + self.post
        )
        channels = max(s.shape[0] for s in sources)
        target = target or np.zeros((channels, duration), dtype=dtype)

        end = self.pre
        for i, src in enumerate(sources):
            g0, g1 = gaps[i : i + 2]
            begin = end + g0
            end = begin + src.shape[-1]

            b, e = begin, end
            if g0 < 0:  # Fade in
                fade = -g0
                target[:, b : b + fade] += fader(0, 1, fade) * src[:, :fade]
                b += fade

            if g1 < 0:  # Fade out
                fade = -g1
                target[:, e - fade : e] += fader(1, 0, fade) * src[:, -fade:]
                e -= fade

            target[:, b:e] += src[:, b - begin : e - end or None]

        return target


"""
# Should be elsewhere in a task

overlap: None or any floating point numbers, referenced to the longest item.

These next comments shoul

0 means: all start together
0.5 means: middles of all songs are at same time
1 means: all end together

Negative numbers and numbers bigger than one are possible!
"""
