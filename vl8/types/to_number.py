from . import to_fraction, types
from functools import singledispatch
import xmod


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


xmod(to_number)
