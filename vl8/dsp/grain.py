from dataclasses import dataclass
from fractions import Fraction
from random import Random, _inst

SIZE = Fraction(1024)


@dataclass
class Grain:
    """Grains from within a larger sample, with optional overlaps and
       optional variation"""

    size: Fraction = SIZE
    """Size of each grain, in fractional samples.  Must be non-negative"""

    overlap: Fraction = SIZE / 2
    """Overlap between grains, in fractional samples.  Must be non-negative."""

    distribution: object = Random.uniform
    """A distribution function that takes a `random.Random`, and two values and
       returns a random floating point number in that range."""

    variation: Fraction = 0
    """Variation between grains, in fractional samples.
       Must be less than size."""

    @property
    def stride(self):
        return self.size - self.overlap

    def sizes(self, size, rand=_inst):
        def delta():
            if not self.variation:
                return 0
            return self.distribution(rand, -self.variation, self.variation)

        begin = 0
        while begin < size:
            end = begin + self.size
            if self.variation:
                end += self.distribution(rand, -self.variation, self.variation)

            yield round(begin), round(min(size, end))
            begin = end - self.overlap

    def grains(self, data, rand=_inst):
        for begin, end in self.sizes(max(data.shape), rand):
            yield data[:, begin:end]
