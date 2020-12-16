from . import DEFAULT_SAMPLE_RATE
from .external import External
from pathlib import Path

_rubberband = External('rubberband {options} {infile} {outfile}', '--', '=')


def rubberband(
    data,
    sample_rate=DEFAULT_SAMPLE_RATE,
    time=None,
    tempo=None,
    duration=None,
    pitch=None,
    frequency=None,
    timemap=None,
    crisp=None,
    formant=False,
):
    times = sum(t is not None for t in (time, tempo, duration))
    freqs = sum(f is not None for f in (pitch, frequency))

    if times > 1:
        raise ValueError('Can only set one of time, tempo, duration')
    if freqs > 1:
        raise ValueError('Can only set one of pitch, frequency')

    if timemap and not Path(timemap).exists():
        raise ValueError('File {timemap} does not exist')

    if not (times or freqs or timemap):
        raise ValueError('No change requested')

    kwargs = {k: v for k, v in locals().items() if v is not None}
    return _rubberband(**kwargs)
