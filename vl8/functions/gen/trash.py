from dataclasses import dataclass
from vl8.function.generator import Generator
import numpy as np


@dataclass
class Trash(Generator):
    _make = staticmethod(np.empty)
