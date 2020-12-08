from dataclasses import dataclass
import functools
import numpy as np


@dataclass
class Fader:
    n_in: int
    n_out: int = 0
    begin: float = 0.0
    end: float = 1.0
    dtype: np.dtype = np.float32
    space: object = np.linspace

    def __post_init__(self):
        lin = functools.partial(self.space, endpoint=True, dtype=self.dtype)

        if self.n_out <= 0:
            self.n_out = self.n_in

        b = self.begin
        e = self.end

        self._fade_in = lin(b, e, self.n_in)
        if self.n_out == self.n_in:
            self._fade_out = lin(e, b, self.n_out)
        else:
            self._fade_out = np.flip(self._fade_in)

    def __call__(self, chunk, target=None):
        a, b, c = self.parts(chunk)

        a = a * self.fade_in
        c = c * self.fade_out

        if target is None:
            return np.c_[a, b, c]

        ta, tb, tc = self.parts(target, self.size)

        ta += a
        tb += b
        tc += c

        return target

    def _parts(self, a, length=0):
        length = length or a.shape[-1]

        i = self.n_in
        o = length - self.n_out

        return a[:, :i], a[:, i:o], a[:, :o]
