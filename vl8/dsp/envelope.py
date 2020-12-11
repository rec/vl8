from dataclasses import dataclass
from numbers import Number
import numpy as np


@dataclass
class Envelope:
    levels: object
    times: object = None
    length: int = None
    loop_count: int = None
    mult: float = None
    offset: float = None
    curve: object = np.linspace

    # reverse: bool = False
    # switch: bool = False

    def __call__(self, source, target):
        levels, times = _check(self.levels, self.times)
        if len(levels) == 1:
            # A constant value
            target += self.scale(source)
            return target

        length = min(i.shape[-1] for i in (source, target))
        if self.length is not None:
            length = min(self.length, length)

        segments = _segments(levels, times, self.loop_count)

        for t, seg in _curves(segments, length, self.curve, source.dtype):
            src = source[:, t : t + len(seg)] * self.scale(seg)
            target[:, t : t + len(seg)] += src

    def scale(self, a):
        if self.mult is not None:
            a = a * self.mult
        if self.offset is not None:
            a = a + self.offset
        return a


def _check(levels, times):
    try:
        level_time_pairs = all(len(i) == 2 for i in levels)
    except Exception:
        level_time_pairs = False

    if times is None:
        if not level_time_pairs:
            raise ValueError(
                'levels must be a list of time, level pairs if times is None'
            )
        times, levels = zip(*levels)
    elif level_time_pairs:
        raise ValueError(
            'times must be None if levels us be a list of time, level pairs'
        )

    if isinstance(levels, Number):
        levels = [levels]
    elif len(levels) < 1:
        raise ValueError('There must be at least one level')

    if isinstance(times, Number):
        times = [times]
    elif not times and len(levels) != 1:
        raise ValueError('A constant envelope can only have one level')

    if any(t < 0 for t in times):
        raise ValueError('Times cannot be negative')

    return levels, times


def _segments(levels, times, loop_count):
    i = 0
    while loop_count is None or i / len(levels) < loop_count:
        yield (
            levels[i % len(levels)],
            levels[(i + 1) % len(levels)],
            times[i % len(times)],
        )
        i += 1


def _curves(segments, length, curve, dtype):
    t = 0
    for l0, l1, dt in segments:
        seg = curve(l0, l1, dt, dtype=dtype, endpoint=True)
        to_chop = t + dt - length
        if to_chop > 0:
            yield t, seg[:-to_chop]
            break
        yield t, seg
        t += dt
