from . import DEFAULT_SAMPLE_RATE
from . import pydub_io
from . import soundfile_io
from . import wavemap_io


# This is obsolete for now
def choose_read(filename):
    exceptions = []

    for module in wavemap_io, pydub_io, soundfile_io:
        try:
            return module.read(filename)
        except Exception as e:
            exceptions.append(str(e))

    raise ValueError(f"Cannot read file {filename}: {exceptions}")


def choose_write(filename, data, sample_rate=DEFAULT_SAMPLE_RATE):
    exceptions = []
    for module in pydub_io, wavemap_io, soundfile_io:
        try:
            return module.write(filename, sample_rate)
        except Exception as e:
            exceptions.append(e)

    raise ValueError(f"Cannot write file {filename}: {exceptions}")
