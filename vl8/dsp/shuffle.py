from .grain import Grain
from dataclasses import dataclass, factory
import random


@dataclass
class Shuffle:
    """Generic shuffler"""

    grain: Grain = factory(Grain)
    shuffle: object = random.shuffle
    seed: int = None

    def __call__(self, source, target):
        if self.seed is not None:
            random.seed(self.seed)
        items = []
        self.shuffle(items)
