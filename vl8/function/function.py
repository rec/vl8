from . import importer
from enum import Enum
import inspect

DEFAULT = 'cat'


class Function:
    class Type(Enum):
        GENERATOR = 'generator'
        SIMPLE = 'simple'
        MULTIPLE = 'multiple'

    def __init__(self, name):
        self.name = name or DEFAULT
        self.function = importer(self.name)
        self.params = _params(self.function)
        self.is_class = isinstance(self.function, type)
        p = self._param()
        if not p:
            self.type = Function.Type.GENERATOR

        elif p.kind is p.VAR_POSITIONAL:
            self.type = Function.Type.MULTIPLE

        elif _is_positional(p):
            self.type = Function.Type.SIMPLE

        else:
            raise ValueError(
                f'Bad signature for {self.function}({self.params})'
            )

    def __str__(self):
        return f'Function({self.function}, {self.params}, {self.type})'

    def required(self):
        return [p.name for p in self.params.values() if p.default is p.empty]

    def _param(self):
        if self.is_class:
            f_call = _get_call(self.function)
            if not f_call:
                raise ValueError(f'Class {self.name} is not callable')

            call_params = list(_params(f_call).values())
            if call_params and call_params[0].name == 'self':
                call_params.pop(0)

            if len(call_params) > 1:
                raise ValueError(
                    f'{self.function}.__call__() takes zero or '
                    f'one argument: {call_params}'
                )
            return call_params and call_params[0]

        elif self.params:
            pname = next(iter(self.params))
            p = self.params[pname]
            if _is_positional(p):
                self.params.pop(pname)
                return p

    def __call__(self, *sources, **kwargs):
        if self.type is Function.Type.SIMPLE and len(sources) != 1:
            raise TypeError(f'{self.name} takes exactly one argument')
        if self.type is Function.Type.GENERATOR and sources:
            raise TypeError(f'{self.name} takes no sources')
        if self.is_class:
            return self.function(**kwargs)(*sources)
        else:
            return self.function(*sources, **kwargs)


def _is_positional(p):
    return p.kind in (
        p.POSITIONAL_ONLY,
        p.POSITIONAL_OR_KEYWORD,
        p.VAR_POSITIONAL,
    )


def _params(s):
    return dict(inspect.signature(s).parameters)


def _get_call(cls):
    x = vars(cls).get('__call__')
    if x:
        return x
    for base in cls.__bases__:
        x = _get_call(base)
        if x:
            return x
