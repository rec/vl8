from dataclasses import dataclass
from pydub import AudioSegment
import functools
import numpy as np


@dataclass
class Sample:
    sample: np.ndarray
    frame_rate: int

    @classmethod
    def read(cls, filename):
        s = AudioSegment.from_file(filename)
        array = np.frombuffer(s._data, dtype=s.array_type)

        assert len(array) == int(s.frame_count())
        assert not len(array) % s.channels

        nsamples = len(array) // s.channels
        matrix = array.reshape(s.channels, nsamples, 'F')

        return cls(matrix, s.frame_rate)

    @functools.wraps(AudioSegment.export)
    def write(self, *args, **kwargs):
        AudioSegment(
            data=self.sample.tobytes('F'),
            sample_width=self.sample.dtype.itemsize,
            frame_rate=self.frame_rate,
            channels=self.sample.shape[1],
        ).export(*args, **kwargs)
