from .types import Numeric
from fractions import Fraction
from functools import singledispatch
import xmod

LIMIT_DENOMINATOR = 1000000


@singledispatch
def to_fraction(ratio: Numeric) -> Fraction:
    raise TypeError(f"Do not understand {ratio} of type {type(ratio)}")


@to_fraction.register(Fraction)
def _(ratio: Fraction) -> Fraction:
    return ratio


@to_fraction.register(int)
def _(ratio: int) -> Fraction:
    return Fraction(ratio)


@to_fraction.register(float)
def _(ratio: float) -> Fraction:
    return _fraction(ratio)


@to_fraction.register(str)
def _(ratio: str) -> Fraction:
    parts = ratio.strip().split("/", maxsplit=1)
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

    f = Fraction(*(to_number(a) for a in args))
    return f.limit_denominator(LIMIT_DENOMINATOR)


xmod(to_fraction)
