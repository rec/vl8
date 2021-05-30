from . import to_fraction
from .types import Number, Numeric
from functools import singledispatch
import xmod


@singledispatch
def to_number(n: Numeric) -> Number:
    return to_fraction(n)


@to_number.register(float)
def _(n: float) -> float:
    return n


@to_number.register(str)
def _(n: str) -> Number:
    if '/' in n:
        return to_fraction(n)
    try:
        return int(n)
    except Exception:
        return float(n)


xmod(to_number)
