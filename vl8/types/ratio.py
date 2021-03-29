from . import types
from functools import singledispatch

LIMIT_DENOMINATOR = 1000000


@singledispatch
def to_fraction(ratio) -> types.Fraction:
    raise TypeError(f'Do not understand {ratio} of type {type(ratio)}')


@to_fraction.register(types.Fraction)
def _(ratio: types.Fraction) -> types.Fraction:
    return ratio


@to_fraction.register(int)
def _(ratio: int) -> types.Fraction:
    return types.Fraction(ratio)


@to_fraction.register(float)
def _(ratio: float) -> types.Fraction:
    return _fraction(ratio)


@to_fraction.register(list)
@to_fraction.register(tuple)
def _(ratio: types.Sequence[int]) -> types.Fraction:
    return _fraction(*ratio)


@to_fraction.register(str)
def _(ratio: str) -> types.Fraction:
    parts = ratio.strip().split('/', maxsplit=1)
    return _fraction(*parts)


@singledispatch
def to_number(n) -> types.Number:
    return to_fraction(n)


@to_number.register(float)
def _(n: float) -> float:
    return n


@to_number.register(str)
def _(n: str) -> types.Number:
    if '/' in n:
        return to_fraction(n)
    try:
        return int(n)
    except Exception:
        return float(n)


def _fraction(*args):
    f = types.Fraction(*(to_number(a) for a in args))
    return f.limit_denominator(LIMIT_DENOMINATOR)
