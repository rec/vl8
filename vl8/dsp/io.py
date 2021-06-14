from . import pydub_io
from pathlib import Path
import datetime
import wavemap

read = pydub_io.read
write = pydub_io.write
DEFAULT_DIR = '_VL8'


def write_data(
    data_list,  # This gets consumed and the samples overwritten
    output_file=None,
    output_format='.wav',
    dtype=None,
    split=False,
    align: float = 0.0,  # Everything starts together
):
    out = output_file or _timestamp()
    if not out.endswith(output_format):
        out += output_format

    if split:
        if '{}' not in out:
            out = '+{}.'.join(out.rsplit('.', maxsplit=1))
        for i, data in enumerate(data_list):
            yield _write(out.format(i + 1), data, dtype)
        return

    input_channels = []
    nchannels = max(d.nchannels for d in data_list)
    nsamples = max(d.nsamples for d in data_list)

    if not nchannels:
        raise ValueError('Empty data_list')
    if nchannels > 2:
        raise NotImplementedError

    longest = (d for d in data_list if d.shape == (nchannels, nsamples))
    target = next(longest, None)
    data = [s for s in data_list if s is not target]

    if target is None:
        target = np.zeros((nchannels, nsamples), dtype=dtype or data[0].dtype)

    for d in data:
        align = max(0, min(1, align))
        o = round(align * (nsamples - d.nsamples))
        target[:, o : o + d.nsamples] += d

    if


    yield _write(out, longest, dtype)




def _prepare(durations):
    durations = [s.shape[1] for s in src]
    maxl, minl = max(durations), min(durations)

    begin = self.center * (maxl - minl) / 2

    self.nlength = maxl
    if begin < 0:
        self.offset = -begin
        return maxl + self.offset
    else:
        self.offset = 0
        return max(maxl, begin + minl)



def _write(filename, data, dtype):
    d = wavemap.convert(data.data, dtype)
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    pydub_io.write(filename, d, data.sample_rate)
    return filename


def _unused_mix_beyond_stereo(channels, data_list, channels_in, exact):
    # default is 1, 2, mixdown to 2 for greater than 2.
    # Also "split" - one file per output
    # Also "=2" - exactly 2 channels
    total_channels = sum(input_channels)
    exact = channels.startswith('=')

    if channels == '*':
        channels_out = len(data_list)
    elif channels = '+':
        channels_out = sum(total_channels)
    elif exact:
        channels_out = int(channels[1:])
    else:
        channels_out = int(channels)

    if not exact:
        channels_out = min(channels_in, channels_out) or total_channels


def _timestamp():
    return datetime.datetime.now().strftime(f'{DEFAULT_DIR}/%Y%m%d-%H%M%S')
