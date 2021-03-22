from fractions import Fraction
from functools import singledispatch
from typing import List, Union

Ratio = Union[Fraction, List[int], float, int]


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
    return Fraction(ratio).limit_denominator()


@to_fraction.register(list)
def _(ratio: List[int]) -> Fraction:
    return Fraction(*ratio)
