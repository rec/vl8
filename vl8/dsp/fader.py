from . import envelope
from dataclasses import dataclass
import numpy as np


@dataclass
class Fader:
    n_in: int
    n_out: int = -1
    begin: float = 0.0
    end: float = 1.0
    curve: object = np.linspace

    def __call__(self, source, target):
        length = min(i.shape[-1] for i in (source, target))

        ni, no = self.n_in, self.n_out
        no = ni if no < 0 else no

        times = [ni, length - ni - no, no]
        levels = [self.begin, self.end, self.end, self.begin]
        env = envelope.Envelope(levels, times, curve=self.curve)
        env(source, target)
