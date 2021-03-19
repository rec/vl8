from ..function.creator import Creator
from dataclasses import dataclass


@dataclass
class AtOnce(Creator):
    overlap: float = 0.5

    def _prepare(self, src):
        self.max_length = max(len(s) for s in src)
        min_length = min(len(s) for s in src)

        begin = round(self.overlap * (self.max_length - min_length) / 2)
        if begin < 0:
            self.offset = -begin
            return self.max_length + self.offset
        else:
            self.offset = 0
            return max(self.max_length, begin + min_length)

    def _call(self, arr, *src):
        for s in src:
            begin = self.offset
            begin += round(self.overlap * (self.max_length - len(s)) / 2)
            arr[:, begin : begin + len(s)] += s
