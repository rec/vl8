from . import types
from functools import singledispatch
import xmod

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


@to_fraction.register(str)
def _(ratio: str) -> types.Fraction:
    parts = ratio.strip().split('/', maxsplit=1)
    return _fraction(*parts)


def _fraction(*args):
    def to_number(s):
        if not isinstance(s, str):
            return s
        try:
            return int(s)
        except Exception:
            pass
        return float(s)

    f = types.Fraction(*(to_number(a) for a in args))
    return f.limit_denominator(LIMIT_DENOMINATOR)


xmod(to_fraction)
