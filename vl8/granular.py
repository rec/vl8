from . import util
from dataclasses import dataclass
import math
import numpy as np

GRAIN_SIZE = 1024


@dataclass
class Grains:
    data: np.ndarray
    size: int = GRAIN_SIZE
    overlap: float = 1.0
    dtype: np.dtype = np.float32

    def __post_init__(self):
        assert 0 <= self.overlap <= 1
        self.fade = round(self.overlap * self.size / 2)
        self.fade_in = np.linspace(
            0, 1, self.fade, endpoint=True, dtype=self.dtype
        )
        self.fade_out = np.flip(self.fade_in)

    def chunk(self, i):
        begin = i * (self.size - self.fade)
        c = self.data[:, begin : begin + self.size]
        missing = self.size - c.shape[1]
        if missing > 0:
            c = np.c_[c, np.zeros((2, missing), dtype=self.dtype)]

        return c

    def add_to(self, i, target):
        c = self.chunk(i)
        f = self.fade

        target[:, :f] += c[:, :f] * self.fade_in
        target[:, f : self.size - f] += c[:, f:-f]
        target[:, self.size - f : self.size] += c[:, -f:]


def grains(data, grain_size, overlap=0):
    assert 0 <= overlap < 1
    grain_overlap = grain_size * overlap
    grain_progress = grain_size - grain_overlap
    grains = math.ceil(data.shape[1] / grain_progress)
    return grains


@dataclass
class Granulator:
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

        fade_in = util.linspace(0, 1, half)
        fade_out = np.flip(fade_in)

        for out_index, (in_index, value) in enumerate(results):
            i = round(in_index) * half
            o = out_index * half
            out[:, o : o + half] += buf[:, i : i + half] * fade_in

            i += half
            o += half
            out[:, o : o + half] += buf[:, i : i + half] * fade_out

        return out
