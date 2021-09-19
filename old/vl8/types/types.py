from fractions import Fraction
from typing import List, Sequence, Union

ExactNumber = Union[int, Fraction]
NonInteger = Union[float, Fraction]
Number = Union[int, float, Fraction]

NumberList = List[Number]
Numeric = Union[Number, str]
NumericSequence = Union[None, Numeric, Sequence[Numeric]]
