from . import types, to_number, to_number_list, to_fraction
import dataclasses
import xmod

_PROPERTY_MAKERS = {
    types.Numeric: to_number,
    types.NumericSequence: to_number_list,
    types.ExactNumber: to_fraction,
}


@xmod
def prop(cls, exclude=(), include=None):
    def make_prop(name, converter):
        def getter(self):
            return getattr(self, name)

        def setter(self, x):
            setattr(self, name, converter(x))

        return property(getter, setter)

    for f in dataclasses.fields(cls):
        if f.name not in exclude and (include is None or f.name in exclude):
            maker = _PROPERTY_MAKERS.get(f.type)
            if maker:
                prop = make_prop('_' + f.name, maker)
                setattr(cls, f.name, prop)
