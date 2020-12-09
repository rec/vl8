from dataclasses import dataclass
import numpy as np


def min_length(*items):
    return min(i.shape[-1] for i in items if i is not None)


@dataclass
class Envelope:
    levels: object
    times: object
    length: int = -1
    loop_count: int = -1
    mult: float = 1
    offset: float = 0
    curve: object = np.linspace

    # reverse: bool = False
    # switch: bool = False

    def __call__(self, source, target=None):
        length = min_length(source, target)
        if self.length >= 0:
            length = min(self.length, length)
        results = []

        segments = _segments(self.times, self.levels, self.loop_count)
        for t, seg in _curves(segments, length, self.curve, source.dtype):
            if self.mult != 1:
                seg = seg * self.mult
            if self.offset != 0:
                seg = seg + self.offset

            if target is None:
                results.append(seg)
            else:
                target[:, t : t + len(seg)] += seg

        return np.c_[results] if target is None else target


def _segments(times, levels, loop_count):
    def to_list(x):
        try:
            return list(x)
        except TypeError:
            return [x]

    times = to_list(times)
    levels = to_list(levels)

    i = 0
    while not (i / len(times) >= loop_count >= 0):
        dt = times[i % len(times)]
        l0 = levels[i % len(levels)]
        l1 = levels[(i + 1) % len(levels)]

        yield l0, l1, dt
        i += 1


def _curves(segments, length, curve, dtype):
    t = 0
    for l0, l1, dt in segments:
        seg = curve(l0, l1, dt, dtype=dtype)
        to_chop = t + dt - length
        if to_chop > 0:
            yield t, seg[:-to_chop]
            return
        yield t, seg
        t += dt
