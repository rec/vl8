from . import DEFAULT_SAMPLE_RATE
from pathlib import Path
from pydub import AudioSegment
import numpy as np


def read(filename):
    s = AudioSegment.from_file(filename)
    array = np.frombuffer(s._data, dtype=s.array_type)
    nsamples = len(array) // s.channels

    assert not len(array) % s.channels
    assert nsamples == int(s.frame_count())

    matrix = array.reshape((s.channels, nsamples), order='F')
    return matrix, s.frame_rate


def write(filename, data, sample_rate=DEFAULT_SAMPLE_RATE, *args, **kwargs):
    first, *rest = data.shape

    if not np.issubdtype(data.dtype, np.integer):
        m1, m2 = np.amax(data), -np.amin(data)
        m = max(m1, m2)
        if m > 1:
            data = data / m

        data = 0xFFFF * (1 + data) / 2 - 0x8000
        assert np.amax(data) <= 0x7FFF
        assert np.amin(data) >= -0x8000
        data = data.astype(np.int16)

    segment = AudioSegment(
        data=data.tobytes('F'),
        sample_width=data.dtype.itemsize,
        frame_rate=sample_rate,
        channels=first if rest else 1,
    )

    format = Path(filename).suffix[1:]
    return segment.export(filename, format, *args, **kwargs)
