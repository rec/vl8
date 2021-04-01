from ..function.creator import Creator
from ..types.types import NumericSequence
from dataclasses import dataclass
from fractions import Fraction


@dataclass
class AtOnce(Creator):
    center: NumericSequence = Fraction(1, 2)
    scale: bool = True

    def _prepare(self, src):
        durations = [s.shape[1] for s in src]
        maxl, minl = max(durations), min(durations)

        begin = self.center * (maxl - minl) / 2

        self.max_length = maxl
        if begin < 0:
            self.offset = -begin
            return maxl + self.offset
        else:
            self.offset = 0
            return max(maxl, begin + minl)

    def _call(self, arr, *src):
        for s in src:
            begin = self.offset
            begin += round(self.center * (self.max_length - len(s)) / 2)
            if self.scale:
                if 'float' in str(s.dtype):
                    s = s / len(src)
                else:
                    s = s // len(src)
            arr[:, begin : begin + len(s)] += s


def _get(a, i):
    return a or None and a[i % len(a)]
