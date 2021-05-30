from . import to_number
from .types import NumberList, Numeric
from typing import List
from functools import singledispatch
import xmod


@singledispatch
def to_number_list(nl) -> NumberList:
    return [to_number(nl)]


@to_number_list.register(list)
def _(nl: List[Numeric]) -> NumberList:
    return [to_number(n) for n in nl]


@to_number_list.register(str)
def _(n: str) -> NumberList:
    return to_number_list(n.split(','))


@to_number_list.register(type(None))
def _(n: str) -> NumberList:
    return []


xmod(to_number_list)
