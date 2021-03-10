from . import io
from pathlib import Path


class File:
    def __init__(self, name):
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
        return self.sample_rate
