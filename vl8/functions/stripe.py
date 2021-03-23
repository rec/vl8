from ..dsp.grain import Grain
from ..dsp.rand import Rand
from ..function.creator import Creator
from dataclasses import dataclass, field
from fractions import Fraction
import copy
import more_itertools

MIN_GRAIN_SIZE = Fraction(50)
MIN_DURATION = Fraction(1000)


@dataclass
class Stripe(Creator):
    grain: Grain = field(default_factory=Grain)
    rand: Rand = field(default_factory=Rand)

    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    def _prepare(self, src):
        if self.grain.size < MIN_GRAIN_SIZE:
            msg = f'Grain too short: {self.grain.size} < {MIN_GRAIN_SIZE}'
            raise ValueError(msg)

        # Add a full extra largest size grain, just in case. :-)
        return sum(s.shape[1] for s in src) + round(self.grain.size)

    def _call(self, arr, *src):
        max_duration = max(s.shape[1] for s in src)
        min_duration = min(s.shape[1] for s in src)

        if min_duration < MIN_DURATION:
            msg = f'Sources too short: {min_duration} < {MIN_DURATION}'
            raise ValueError(msg)

        grain_count = max_duration / self.grain.stride

        # What if some duration is "pretty short"?
        #
        # If one source is 60 minutes = 3600s and another is 1s, with
        # a grain of 50ms, 2200 samples then if I scale that size down to the
        # 1s source then it will be less than one sample long.
        #
        # A hard-limit on stripe size fixes this, but means we must expect to
        # run out of some (short) sources before the end.

        grain_chunks = []
        for s in src:
            duration = max(s.shape)
            grain_size = max(MIN_GRAIN_SIZE, duration / grain_count)
            ratio = grain_size / self.grain.size
            assert ratio <= 1, f'{ratio} > 1'

            grain = copy.copy(self.grain)
            grain.size *= ratio
            grain.overlap *= ratio
            assert (
                MIN_GRAIN_SIZE <= grain.stride <= self.grain.stride
            ), f'{MIN_GRAIN_SIZE} > {grain.stride} > {self.grain.stride}'

            grain_chunks.append(((grain, chunk) for chunk in grain.chunks(s)))

        striped_chunks = more_itertools.interleave_longest(*grain_chunks)
        # striped_chunks = [list(i) for i in il]
        # print(len(striped_chunks))
        # print(*(len(s) for s in striped_chunks))
        # print(*(type(s) for s in striped_chunks[0]))
        time = 0

        for i, (grain, chunk) in enumerate(striped_chunks):
            print(round(time), time, i, chunk.shape)
            rt = round(time)
            arr[:, rt : rt + chunk.shape[1]] += chunk
            time += grain.stride
