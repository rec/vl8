from ..dsp.grain import Grain, GrainSamples
from ..dsp.rand import Rand
from ..function.creator import Creator
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from more_itertools import interleave_longest

MIN_GRAIN_SAMPLES = Fraction(50)
MIN_DURATION = Fraction(1000)


@dataclass
class Stripe(Creator):
    grain: Grain = field(default_factory=Grain)
    rand: Rand = field(default_factory=Rand)
    grow_grains: bool = False

    def _prepare(self, src):
        # Add extra so we can slop over
        return sum(s.shape[1] for s in src) + 1024

    def _call(self, arr, *src):
        sgrain = self.grain.to_samples(src[0].sample_rate)
        durations = [s.shape[1] for s in src]
        min_dur, max_dur = min(durations), max(durations)
        ref_dur = min_dur if self.grow_grains else max_dur
        grain_count = ref_dur / sgrain.stride

        def chunks(s):
            stride = max(MIN_GRAIN_SAMPLES, s.shape[1] / grain_count)
            # ratio = nsamples / sgrain.nsamples
            d = dict(asdict(sgrain), nsamples=stride + sgrain.overlap)
            grain = GrainSamples(**d)
            for chunk in grain.chunks(s):
                yield chunk, grain.stride

        time = 0
        missing_chunk = 0
        total_chunks = 0
        for chunk, stride in interleave_longest(*(chunks(s) for s in src)):
            total_chunks += 1
            rt = round(time)
            if arr.shape[1] < chunk.shape[1] + rt:
                missing_chunk += 1
            else:
                arr[:, rt : rt + chunk.shape[1]] += chunk
            time += stride

        if missing_chunk:
            raise ValueError("missing chunk")

        return arr[:, : round(time)]


# What if some duration is "pretty short"?
#
# If one source is 60 minutes = 3600s and another is 1s, with
# a grain of 50ms, 2200 samples then if I scale that size down to the
# 1s source then it will be less than one sample long.
#
# A hard-limit on stripe size fixes this, but means we must expect to
# run out of some (short) sources before the end.
