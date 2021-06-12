from . import to_fraction, to_number, units
from .types import Number, Numeric, ExactNumber
from fractions import Fraction
from functools import singledispatch
from typing import Sequence


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
    if True:
        raise ValueError('This is deprecated!')
    return to_fraction(duration)


@_convert.register(str)
def _(duration: str, sample_rate: int) -> Number:
    # Examples: '2', '2.3', '23 / 10', '300 samples', '300s', '300ms'
    value, scale = units.split(duration, sample_rate)
    return to_number(value) / scale
