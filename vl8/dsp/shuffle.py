from .grain import Grain
from .rand import Rand
from dataclasses import dataclass, field
from typing import Callable
import numpy as np
import random


@dataclass
class Shuffle:
    """Generic shuffler"""

    grain: Grain = field(default_factory=Grain)
    shuffle: Callable = random.Random.shuffle
    rand: Rand = field(default_factory=Rand)

    def __call__(self, source: np.darray, target: np.darray):
        self.shuffle(source)  # TODO
