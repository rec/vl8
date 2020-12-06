from dataclasses import dataclass
from pathlib import Path
from pydub import AudioSegment
import functools
import numpy as np

DEFAULT_SAMPLE_RATE = 44100


@dataclass
class Sample:
    data: np.ndarray
    sample_rate: int = DEFAULT_SAMPLE_RATE

    def __post_init__(self):
        length, *rest = self.data.shape
        if not rest:
            self.data = self.data.reshape((1, length))

    def to_time(self, samples):
        return samples / self.sample_rate

    def to_samples(self, time):
        return round(time * self.sample_rate)

    @property
    def channels(self):
        return self.data.shape[0]

    def __len__(self):
        return self.data.shape[1]

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
            frame_rate=self.sample_rate,
            channels=self.channels,
        )
