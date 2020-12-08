from dataclasses import dataclass
import numpy as np


@dataclass
class Envelope:
    levels: object
    times: object
    length: int = None
    loop_count: int = -1
    mult: float = 1
    offset: float = 0
    # reverse: bool = False
    # switch: bool = False

    def __iter__(self):
        def to_list(x):
            try:
                return list(x)
            except TypeError:
                return [x]

        times = to_list(self.times)
        levels = to_list(self.levels)

        i = 0
        while not (i / len(times) >= self.loop_count >= 0):
            dt = times[i % len(times)]
            l0 = levels[i % len(levels)]
            l1 = levels[(i + 1) % len(levels)]

            yield l0, l1, dt
            i += 1

    def _segments(self, length, space, dtype):
        t = 0
        for l0, l1, dt in self:
            seg = space(l0, l1, dt, dtype=dtype)
            to_chop = t + dt - length
            if to_chop > 0:
                yield t, seg[:-to_chop]
                return
            yield t, seg
            t += dt

    def __call__(self, source, target=None, space=np.linspace):
        length = min(t.shape[-1] for t in (source, target) if t is not None)
        segments = []

        for t, seg in self._segments(length, space, source.dtype):
            if target is None:
                segments.append(seg)
            else:
                target[:, t : t + len(seg)] += seg
