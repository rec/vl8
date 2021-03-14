from . import io
from dataclasses import dataclass
from pathlib import Path
import numpy as np


class HasData:
    def apply(self, operation):
        return Data(operation(self), self.sample_rate)


@dataclass
class Data(HasData):
    def __init__(self, data: np.ndarray, sample_rate: int):
        self.data = data
        self.sample_rate = sample_rate


class File(HasData):
    def __init__(self, name: str):
        self.path = Path(name).absolute()
        if not self.path.exists():
            raise FileNotFoundError(f"No such file or directory {name}")
        self._data = None
        self._sample_rate = None

    @property
    def data(self):
        if self._data is None:
            self._data, self._sample_rate = io.read(self.path)
        return self._data

    @property
    def sample_rate(self):
        self.data
        return self._sample_rate
