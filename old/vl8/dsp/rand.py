from .scale import Scale
from dataclasses import dataclass, field
from numpy.random import Generator, default_rng
from typing import Callable, Optional, Union

Distribution = Union[Callable, str, None]
DEFAULT_DISTRIBUTION = 'uniform'


@dataclass
class Rand:
    distribution: Distribution = None
    args: list = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)
    seed: Optional[int] = None
    scale: Scale = field(default_factory=Scale)

    def __post_init__(self):
        self._inst = default_rng(self.seed)

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

    def _set_distribution(self, d: Distribution):
        d = DEFAULT_DISTRIBUTION if d is None else d
        if callable(d):
            self._distribution = d
        else:
            try:
                self._distribution = getattr(Generator, d)
            except AttributeError:
                raise ValueError(f'No distribution {d}') from None

    def _get_distribution(self) -> Callable:
        return self._distribution


Rand.distribution = property(Rand._get_distribution, Rand._set_distribution)
