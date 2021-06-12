from . import io
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import wavemap


class HasData:
    def apply(self, operation):
        return Data(operation(self), self.sample_rate)

    def __getattr__(self, k: str) -> object:
        return getattr(self.data, k)

    floating_dtype = np.dtype('float32')

    @property
    def floating(self):
        if getattr(self, '_floating', None) is None:
            if 'float' in str(self.data.dtype):
                self._floating = self.data
            else:
                self._floating = wavemap.convert(
                    self.data, self.floating_dtype
                )
        return self._floating

    @property
    def nchannels(self):
        return self.data.shape[0]

    @property
    def nsamples(self):
        return self.data.shape[1]

    def __getitem__(self, k):
        return self.data[k]


@dataclass
class Data(HasData):
    data: np.ndarray
    sample_rate: int


class File(HasData):
    def __init__(self, name: str):
        self.path = Path(name).absolute()
        if not self.path.exists():
            raise FileNotFoundError(f"No such file or directory {name}")

        self._data = self._sample_rate = None

    @property
    def data(self):
        if self._data is None:
            self._data, self._sample_rate = io.read(self.path)
        return self._data

    @data.setter
    def data(self, data):
        self._floating = None
        if data is None:
            self._data = self._sample_rate = None
        else:
            self._sample_rate = data.sample_rate
            self._data = data.data

    @property
    def sample_rate(self):
        self.data
        return self._sample_rate
