from ..dsp.grain import Grain
from ..dsp.rand import Rand
from ..function.creator import Creator
from dataclasses import dataclass, field
from fractions import Fraction
from more_itertools import interleave_longest

MIN_GRAIN_SAMPLES = Fraction(50)
MIN_DURATION = Fraction(1000)


@dataclass
class Stripe(Creator):
    grain: Grain = field(default_factory=Grain)
    rand: Rand = field(default_factory=Rand)
    grow_grains: bool = False

    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    def _prepare(self, src):
        # Add a full extra largest size grain, just in case. :-)
        return sum(s.shape[1] for s in src) + 1024

    def _call(self, arr, *src):
        sgrain = self.grain.to_samples(src[0].sample_rate)
        durations = [s.shape[1] for s in src]
        min_dur, max_dur = min(durations), max(durations)
        ref_dur = min_dur if self.grow_grains else max_dur
        grain_count = ref_dur / sgrain.stride

        def chunks(s):
            sample_count = max(MIN_GRAIN_SAMPLES, s.shape[1] / grain_count)
            # ratio = sample_count / sgrain.sample_count
            d = dict(sgrain.asdict(), sample_count=sample_count)
            grain = Grain(**d)
            for chunk in grain.chunks(s):
                yield chunk, grain.stride

        time = 0
        for chunk, stride in interleave_longest(*(chunks(s) for s in src)):
            # print(round(time), time, i, chunk.shape)
            rt = round(time)
            arr[:, rt : rt + chunk.shape[1]] += chunk
            time += stride


# What if some duration is "pretty short"?
#
# If one source is 60 minutes = 3600s and another is 1s, with
# a grain of 50ms, 2200 samples then if I scale that size down to the
# 1s source then it will be less than one sample long.
#
# A hard-limit on stripe size fixes this, but means we must expect to
# run out of some (short) sources before the end.
