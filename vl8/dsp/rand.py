from .scale import Scale
from dataclasses import dataclass, field
from typing import Callable, Optional
import random


@dataclass
class Rand:
    distribution: Callable = random.Random.uniform
    args: list = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)
    seed: Optional[int] = None
    scale: Scale = field(default_factory=Scale)

    def __post_init__(self):
        self._inst = random.Random()
        if self.seed is not None:
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

        return self.scale(self.distribution(self._inst, *args, **kwargs))
