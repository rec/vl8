from . import to_number, types
from functools import singledispatch
import xmod


@singledispatch
def to_number_list(nl) -> types.NumberList:
    return [to_number(nl)]


@to_number_list.register(list)
@to_number_list.register(tuple)
def _(nl) -> types.NumberList:
    return [to_number(n) for n in nl]


@to_number_list.register(str)
def _(n: str) -> types.Number:
    return to_number_list(n.split(','))


xmod(to_number_list)
