from dataclasses import dataclass
import random

SIZE = 1024
OVERLAP = 0.5


@dataclass
class Grain:
    """Grains from within a larger sample, with optional overlaps and
    optional variation"""

    size: int = SIZE
    """Size of each grain, in samples"""

    overlap: float = OVERLAP
    """Overlap between grains, as a ratio to `size`"""

    variation: float = 0.0
    """Variation between grains, as a ratio to `size`"""

    seed: int = None
    """Seed for random.seed"""

    distribution: object = random.uniform
    """A distribution function that takes two values and returns a random
    number in that range."""

    @property
    def fade(self):
        return round(self.overlap * self.size / 2)

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
            if begin >= length:
                break
            yield data[:, begin:end]
