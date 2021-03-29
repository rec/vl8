from fractions import Fraction
from typing import List, Sequence, Union

ExactNumber = Union[Fraction, int]
NonInteger = Union[Fraction, float]
Number = Union[NonInteger, int]
Numeric = Union[Number, Sequence[int], str]
NumberList = List[Number]
