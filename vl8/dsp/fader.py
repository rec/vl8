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

    def __call__(self, source, target=None):
        if target is None:
            target = np.empty_like(source)

        ni = self.n_in
        no = self.n_out or ni

        length = min(i.shape[-1] for i in (source, target))
        times = [ni, length - no, length]
        levels = [self.begin, self.end, self.begin]

        env = envelope.Envelope(levels, times, curve=self.curve)
        return env(source, target)
