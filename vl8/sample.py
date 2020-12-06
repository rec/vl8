from dataclasses import dataclass
from pathlib import Path
from pydub import AudioSegment
import functools
import numpy as np


@dataclass
class Sample:
    data: np.ndarray
    frame_rate: int

    def __post_init__(self):
        length, *rest = self.data.shape
        if not rest:
            self.data = self.data.reshape((1, length))

    @classmethod
    def read(cls, filename):
        s = AudioSegment.from_file(filename)
        array = np.frombuffer(s._data, dtype=s.array_type)
        nsamples = len(array) // s.channels

        assert not len(array) % s.channels
        assert nsamples == int(s.frame_count())

        matrix = array.reshape((s.channels, nsamples), order='F')
        return cls(matrix, s.frame_rate)

    @functools.wraps(AudioSegment.export)
    def write(self, out_f, format=None, *args, **kwargs):
        format = format or Path(out_f).suffix[1:]
        return self.segment().export(out_f, format, *args, **kwargs)

    def segment(self):
        return AudioSegment(
            data=self.data.tobytes('F'),
            sample_width=self.data.dtype.itemsize,
            frame_rate=self.frame_rate,
            channels=self.data.shape[0],
        )
