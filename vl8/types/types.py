from fractions import Fraction
from typing import List, Sequence, Union

ExactNumber = Union[int, Fraction]
NonInteger = Union[float, Fraction]
Number = Union[int, float, Fraction]

NumberList = List[Number]

# TODO: do we really want Sequence[int] now we have str?
Numeric = Union[Number, str, Sequence[int]]
NumericSequence = Union[None, Numeric, Sequence[Numeric]]
