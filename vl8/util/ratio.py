from fractions import Fraction
from functools import singledispatch
from typing import Sequence, Union

ExactNumber = Union[Fraction, int]
NonInteger = Union[Fraction, float]
Number = Union[NonInteger, int]
Numeric = Union[Number, Sequence[int], str]

LIMIT_DENOMINATOR = 1000000


@singledispatch
def to_fraction(ratio) -> Fraction:
    raise TypeError(f'Do not understand {ratio} of type {type(ratio)}')


@to_fraction.register(Fraction)
def _(ratio: Fraction) -> Fraction:
    return ratio


@to_fraction.register(int)
def _(ratio: int) -> Fraction:
    return Fraction(ratio)


@to_fraction.register(float)
def _(ratio: float) -> Fraction:
    return _fraction(ratio)


@to_fraction.register(list)
@to_fraction.register(tuple)
def _(ratio: Sequence[int]) -> Fraction:
    return _fraction(*ratio)


@to_fraction.register(str)
def _(ratio: str) -> Fraction:
    parts = ratio.strip().split('/', maxsplit=1)
    return _fraction(*parts)


def to_number(x: Union[str, Number]) -> Number:
    if not isinstance(x, str):
        return x
    try:
        return int(x)
    except Exception:
        return float(x)


def _fraction(*args):
    f = Fraction(*(to_number(a) for a in args))
    return f.limit_denominator(LIMIT_DENOMINATOR)
