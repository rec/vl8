from . import npf
from pydub import AudioSegment


def read(filenames, grain_size=0, gap=0):
    segments = [AudioSegment.from_file(f) for f in filenames]
    frame_rates = {s.frame_rate() for s in segments}
    if len(frame_rates) > 1:
        raise ValueError(f'Multiple frame rates {frame_rates}')
    frame_rate = frame_rates.pop()

    channels = {s.channel() for s in segments}
    if len(channels) > 1:
        raise ValueError(f'Multiple channel widths {channels}')
    # channel = channels.pop()

    duration = sum(int(s.frame_count()) for s in segments)
    duration += gap * (len(filenames) - 1)

    fill = grain_size and -duration % grain_size
    if fill:
        buffer = npf.empty(duration + fill)
        buffer[:, -fill:].fill(0)
    else:
        buffer = npf.empty(duration)

    begin = 0
    while segments:
        segment = segments.pop(0)
        nsamples = int(segment.frame_count())
        end = begin + nsamples

        chunk = npf.frombuffer(segment._data, dtype=segment.array_type)
        chunk = chunk.reshape(nsamples, segment.channels)
        chunk.transpose().astype(npf.float32)
        buffer[:, begin:end] = chunk
        begin = end + gap

    return buffer, frame_rate
