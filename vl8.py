"""
🏃 Run one or more commands 🏃
------------------------------------------------------------------
"""


# import stroll
from dataclasses import dataclass
import numpy as np
import util

__all__ = 'vl8'
__version__ = '0.2.0'
INFILE = '/data/vl8/full.wav'
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
    duration: int = 0

    def __post_init__(self):
        assert not (self.grain_size % 2)
        self.buffer = util.read(self.filename, self.grain_size, self.duration)
        self.duration = self.buffer.shape[1]

    def run(self, function, outfile):
        results = self.for_each_granule(function)
        results.sort(1)
        print('writing', outfile)
        util.write(outfile, self.combine(results))

    def for_each_granule(self, function):
        half = self.grain_size // 2
        granules = self.duration // half
        granules = round(granules)

        results = util.empty(granules).transpose()
        for i in range(granules):
            begin = half * i
            end = begin + self.grain_size
            value = function(self.buffer[:, begin:end])
            results[i] = float(i), value

        return results

    def combine(self, results):
        half = self.grain_size // 2
        buf = self.buffer
        out = util.zeros(buf.shape[1] + half)

        fade_in = np.linspace(0, 1, half, dtype=util.FLOAT)
        fade_out = np.flip(fade_in)

        for out_index, (in_index, value) in enumerate(results):
            i = round(in_index) * half
            o = out_index * half
            out[:, o : o + half] += buf[:, i : i + half] * fade_in

            i += half
            o += half
            out[:, o : o + half] += buf[:, i : i + half] * fade_out

        return out


if __name__ == '__main__':
    print('Reading', INFILE)
    generator = Granulator(INFILE)

    print('Running mean_square')
    generator.run(mean_square, '/data/vl8/mean_square.wav')
