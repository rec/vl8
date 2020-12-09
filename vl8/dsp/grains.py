from .fader import Fader
from dataclasses import dataclass
import random

SIZE = 1024
OVERLAP = 0.5


@dataclass
class Grain:
    size: int = SIZE
    overlap: float = OVERLAP
    variation: float = 0.0
    seed: int = None
    distribution: object = random.uniform

    @property
    def fade(self):
        return round(self.overlap * self.size / 2)

    @property
    def fader(self):
        return Fader(self.fade)

    @property
    def stride(self):
        return self.size - self.fade

    def sizes(self):
        v = 0
        if self.variation:
            assert 0 < self.variation < 1
            random.seed(self.seed)
            v = round(self.variation * self.size)

        i = 0
        while True:
            delta = v and self.distribution(-v, v)
            yield i, i + delta + self.size
            i += delta + self.stride

    def grains(self, data):
        length = data.shape[-1]
        for begin, end in self.sizes():
            if begin < length:
                yield self.data[:, begin:end]
            else:
                break
