from ..util import abbrev
from .ratio import Number, Numeric, ExactNumber, to_fraction, to_number
from fractions import Fraction
from functools import singledispatch
from typing import Sequence
import re

_match_units = re.compile(r'^([^a-zA-Z]*)([a-zA-Z]*)$').match


def to_samples(d: Numeric, sample_rate: int) -> ExactNumber:
    return to_fraction(_convert(d, sample_rate) * sample_rate)


def to_seconds(d: Numeric, sample_rate: int = 0) -> Number:
    return _convert(d, sample_rate)


@singledispatch
def _convert(duration: Numeric, sample_rate: int) -> Number:
    return duration


@_convert.register(list)
@_convert.register(tuple)
def _(duration: Sequence[int], sample_rate: int) -> Fraction:
    return to_fraction(duration)


@_convert.register(str)
def _(duration: str, sample_rate: int) -> Number:
    # Examples: '2', '2.3', '23 / 10', '300 samples', '300s', '300ms'
    match = _match_units(duration.strip())
    if not match:
        raise ValueError(f'Bad duration "{duration}"') from None
    value, unit = match.groups()

    try:
        u = abbrev(_UNITS, unit)
    except KeyError:
        raise ValueError(f'Unknown unit "{unit}"') from None

    if u:
        scale = 1 / u
    elif not sample_rate:
        raise ValueError('No sample rate for duration {duration}')
    else:
        scale = sample_rate

    parts = value.split('/', maxsplit=1)
    if len(parts) == 1:
        v = to_number(parts[0])
    else:
        v = to_fraction(parts)
    return v / scale


_MS = Fraction(1, 1000)
_US = _MS / 1000
_NS = _US / 1000

_UNITS = {
    '': Fraction(1),
    's': Fraction(1),
    'seconds': Fraction(1),
    'milliseconds': _MS,
    'mseconds': _MS,
    'microseconds': _US,
    'useconds': _US,
    'µseconds': _US,
    'nanoseconds': _NS,
    'nseconds': _NS,
    'minutes': Fraction(60),
    'hours': Fraction(60 * 60),
    'weeks': Fraction(60 * 60 * 7),
    'years': Fraction(1826211, 5000),
    'samples': Fraction(0),
}
