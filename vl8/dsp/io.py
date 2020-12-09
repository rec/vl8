from pathlib import Path
from pydub import AudioSegment
import numpy as np

DEFAULT_SAMPLE_RATE = 44100


def read(filename):
    s = AudioSegment.from_file(filename)
    array = np.frombuffer(s._data, dtype=s.array_type)
    nsamples = len(array) // s.channels

    assert not len(array) % s.channels
    assert nsamples == int(s.frame_count())

    matrix = array.reshape((s.channels, nsamples), order='F')
    return matrix, s.frame_rate


def write(data, filename, sample_rate=DEFAULT_SAMPLE_RATE, *args, **kwargs):
    first, *rest = data.shape
    segment = AudioSegment(
        data=data.tobytes('F'),
        sample_width=data.dtype.itemsize,
        frame_rate=sample_rate,
        channels=first if rest else 1,
    )

    format = Path(filename).suffix[1:]
    return segment.export(filename, format, *args, **kwargs)
