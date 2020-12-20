from dataclasses import dataclass
from random import Random, _inst

SIZE = 1024
OVERLAP = 0.5


@dataclass
class Grain:
    """Grains from within a larger sample, with optional overlaps and
       optional variation"""

    size: int = SIZE
    """Size of each grain, in samples.  Must be non-negative"""

    overlap: int = SIZE // 2
    """Overlap between grains, in samples.  Must be non-negative."""

    distribution: object = Random.uniform
    """A distribution function that takes a `random.Random`, and two values and
       returns a random floating point number in that range."""

    variation: float = 0.0
    """Variation between grains, as a ratio to `size`.
       Must be between 0 and 1."""

    @property
    def fade(self):
        return self.overlap // 2

    @property
    def stride(self):
        return self.size - self.fade

    def sizes(self, rand=_inst):
        v = 0
        if self.variation:
            assert 0 < self.variation < 1
            v = self.variation * self.size

        i = 0
        while True:
            delta = v and round(self.distribution(rand, -v, v))
            yield i, i + delta + self.size
            i += delta + self.stride

    def grains(self, data, rand=_inst):
        # Dodgy
        length = data.shape[-1]
        for begin, end in self.sizes(rand):
            if begin >= length:
                break
            yield data[:, begin:end]
