from old.vl8.dsp import curve_cache
from old.vl8.function.creator import Creator
from vl8.dsp import fix_gaps
from dataclasses import dataclass


@dataclass
class Catenate(Creator):
    curve: curve_cache.Curve = None
    gap: fix_gaps.Gaps = 0
    pre: int = 0
    post: int = 0

    def _prepare(self, src):
        durations = [s.shape[1] for s in src]
        self.gaps = fix_gaps(
            durations, self.gap, self.pre, self.post, src[0].sample_rate
        )
        return sum(durations) + sum(self.gaps)

    def _call(self, arr, *src):
        """
        gap: None, a number of seconds or a list of seconds
        if a gap is negative, it's a fade
        """

        fader = curve_cache(self.curve, arr.dtype)

        begin = end = 0
        for i, s in enumerate(src):
            begin = end + self.gaps[i]
            end = begin + s.shape[-1]
            fade_in, fade_out = -self.gaps[i], -self.gaps[i + 1]

            b, e = begin, end
            if fade_in > 0:
                delta = fader(0, 1, fade_in) * s[:, :fade_in]
                arr[:, b : b + fade_in] += delta
                b += fade_in

            if fade_out > 0:
                delta = fader(1, 0, fade_out) * s[:, -fade_out:]
                arr[:, e - fade_out : e] += delta
                e -= fade_out

            arr[:, b:e] += s[:, b - begin : e - end or None]


"""
# Should be elsewhere in a task

overlap: None or any floating point numbers, referenced to the longest item.

These next comments shoul

0 means: all start together
0.5 means: middles of all songs are at same time
1 means: all end together

Negative numbers and numbers bigger than one are possible!
"""
