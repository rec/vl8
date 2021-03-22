from fractions import Fraction
from functools import singledispatch
from typing import List, Union

Ratio = Union[Fraction, List[int], float, int, str]
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
def _(ratio: List) -> Fraction:
    return _fraction(*ratio)


@to_fraction.register(str)
def _(ratio: str) -> Fraction:
    parts = ratio.strip().split('/', maxsplit=1)
    return _fraction(*parts)


def _fraction(*args):
    def _num(x):
        if isinstance(x, (float, int)):
            return x
        try:
            return int(x)
        except Exception:
            return float(x)

    f = Fraction(*(_num(a) for a in args))
    return f.limit_denominator(LIMIT_DENOMINATOR)
