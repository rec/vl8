from . import DEFAULT_SAMPLE_RATE
from pathlib import Path
import numpy as np
import soundfile

DEFAULT_TYPE = np.float32

DTYPE = {
    'PCM_16': np.int16,
    'PCM_32': np.int32,
    'DOUBLE': np.float64,
    'FLOAT': np.float32,
}
SPECIAL_DTYPE = {
    'PCM_24': np.int32,
    'PCM_S8': np.int16,
    'PCM_U8': np.int16,
}


def read(file, *args, original_type=True, **kwargs):
    f = _file(file)
    sf = soundfile.SoundFile(f)
    dtype = DTYPE.get(sf.subtype, SPECIAL_DTYPE.get(sf.subtype, DEFAULT_TYPE))
    data, sr = soundfile.read(f, always_2d=True, dtype=dtype, *args, **kwargs)
    data = np.transpose(data)

    if original_type:
        if sf.subtype == 'PCM_S8':
            data /= 0x100
            data = data.astype(np.int8)

        elif sf.subtype == 'PCM_U8':
            data //= 0x100
            data += 0x80
            data = data.astype(np.uint8)

    return data, sr


def write(filename, data, sample_rate=DEFAULT_SAMPLE_RATE, *args, **kwargs):
    d = np.transpose(data)

    f = _file(filename)
    assert f.endswith('.wav')

    if d.dtype == np.int8:
        d = d.astype(np.int16)
        d *= 0x100
    elif d.dtype == np.uint8:
        d = d.astype(np.int16)
        d -= 0x80
        d *= 0x100
    elif d.dtype == np.uint16:
        d = d.astype(np.int16)
        d += 0x8000  # I think

    for subtype, dt in DTYPE.items():
        if dt == d.dtype:
            break
    else:
        raise ValueError(f'Unknown type {d.dtype}')

    return soundfile.write(f, d, sample_rate, subtype, *args, **kwargs)


def _file(f):
    return str(Path(f).absolute())
