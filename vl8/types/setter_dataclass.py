from . import types, to_number, to_number_list, to_fraction
from typing import Optional
import dataclasses
import functools
import xmod


def _optional(fn):
    @functools.wraps(fn)
    def wrapped(x):
        return None if x is None else fn(x)

    return wrapped


_PROPERTY_MAKERS = {
    types.Numeric: to_number,
    types.NumericSequence: to_number_list,
    types.ExactNumber: to_fraction,
}
_PROPERTY_MAKERS.update(
    {Optional[t]: _optional(f) for t, f in _PROPERTY_MAKERS.items()}
)


@xmod
def setter_dataclass(cls, exclude=(), include=None):
    if not dataclasses.is_dataclass(cls):
        cls = dataclasses.dataclass(cls)

    def make_prop(name, converter):
        def getter(self):
            return getattr(self, name)

        def setter(self, x):
            setattr(self, name, converter(x))

        return property(getter, setter)

    for f in dataclasses.fields(cls):
        if f.name not in exclude and (include is None or f.name in include):
            maker = _PROPERTY_MAKERS.get(f.type)
            if maker:
                prop = make_prop('_' + f.name, maker)
                setattr(cls, f.name, prop)

    return cls
