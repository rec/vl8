from dataclasses import dataclass, field
from typing import Callable, Optional
import random


@dataclass
class Rand:
    distribution: Callable = random.Random.uniform
    args: list = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)
    seed: Optional[int] = None
    scale: float = 1
    offset: float = 0

    def __post_init__(self):
        if self.seed is None:
            self._inst = random._inst
        else:
            self._inst = random.Random()
            self._inst.seed(self.seed)

    def __call__(self, *args, **kwargs):
        if not args:
            args = self.args
        elif self.args:
            args = self.args + list(args)
        if not kwargs:
            kwargs = self.kwargs
        elif self.kwargs:
            kwargs = dict(self.kwargs, **kwargs)

        d = self.distribution(self._inst, *args, **kwargs)
        return self.scale * d + self.offset
