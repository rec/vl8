from .grain import Grain, GrainType
from .rand import Rand
from dataclasses import dataclass, field
from typing import Callable
import numpy as np
import random


@dataclass
class Shuffle:
    """Generic shuffler"""

    grain: GrainType = field(default_factory=Grain)
    shuffle: Callable = random.Random.shuffle
    rand: Rand = field(default_factory=Rand)

    def __call__(self, source: np.ndarray, target: np.ndarray):
        self.shuffle(source)  # TODO
