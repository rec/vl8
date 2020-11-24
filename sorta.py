"""
🏃 Run one or more commands 🏃
------------------------------------------------------------------
"""

from dataclasses import dataclass
import aubio
import stroll
import numpy as np
import util

__all__ = 'sorta'
__version__ = '0.1.0'
OUTFILE = '/data/sorta/full.wav'
MAX_FRAME = 4096
SAMPLERATE = 44100
GRAIN_SIZE = SAMPLERATE // 10


def mean_square(granule):
    return np.mean(granule * granule)


@dataclass
class Granulator:
    filename: str
    grain_size: int = GRAIN_SIZE
    sort: bool = True

    def __post_init__(self):
        assert not (self.grain_size % 2)
        self.buffer = util.read(self.filename, self.grain_size)

        begin = 0
        for c in src:
            end = min(duration, begin + chunk.shape[1])
            self.buffer[:, begin : end] = chunk[:, : end - begin]
            begin = enda

    def run(self, function, sort=True):
        results = self.for_each_granule(function)
        if sort:
            results.sort(axis=1)
        return self.combine(results)

    def for_each_granule(self, function):
        half = self.grain_size / 2
        results = empty(self.duration / half).transpose()
        for i, r in enumerate(results):
            begin = half * i
            end = begin + self.grain_size
            r[:] = float(i), function(self.buffer[:, begin:end])

        return results

    def combine(self, results):
        half = self.grain_size / 2
        fade_in = np.linspace(0, 1, half, dtype=util.FLOAT)
        fade_out = np.flip(fade_in)
        buf = self.buffer
        out = zeros(buf.shape[1] + half)

        for out_index, (in_index, value) in enumerate(results):
            i = in_index * half
            o = out_index * half
            out[:, o:o + half] += buf[:, i:i + half] * fade_in

            i += half
            o += half
            out[:, o:o + half] += buf[:, i: i + half] * fade_in

         return out


if __name__ == '__main__':
    print(read_file().shape)
