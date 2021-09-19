from . import pydub_io
from pathlib import Path
import datetime
import wavemap

read = pydub_io.read
write = pydub_io.write
DEFAULT_DIR = '_VL8'


def write_data(data_list, output_file=None, output_format='.wav', dtype=None):
    out = output_file or _timestamp()
    if '.' not in out:
        dot = '' if output_format.startswith('.') else '.'
        out = f'{out}{dot}{output_format}'

    if '{' not in out:
        out = '{}.'.join(out.rsplit('.', maxsplit=1))

    for i, data in enumerate(data_list):
        filename = out.format('' if len(data_list) == 1 else f'+{i}')
        d = wavemap.convert(data.data, dtype)
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        write(filename, d, data.sample_rate)
        yield filename


def _timestamp():
    return datetime.datetime.now().strftime(f'{DEFAULT_DIR}/%Y%m%d-%H%M%S')
