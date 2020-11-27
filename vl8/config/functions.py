from . import ARGS, NAME
import functools
import importlib


def parse(functions):
    for k, v in list(functions.items()):
        if isinstance(v, str):
            v = {NAME: v}
        elif isinstance(v, list):
            v = {NAME: v[0], ARGS: v[1:]}

        if not isinstance(v, dict):
            yield 'function %s was not a string or dict' % k
        elif NAME not in v:
            yield 'function had no _name' % k
        else:
            name = v.pop(NAME)
            args = v.pop(ARGS, [])
            function = _import(name)
            functions[k] = functools.partial(function, *args, **v)


def _import(symbol):
    parts = []
    while True:
        try:
            result = importlib.import_module(symbol)
        except ModuleNotFoundError:
            symbol, *rest = symbol.rsplit('.', maxsplit=1)
            if not rest:
                raise
            parts.insert(0, *rest)
        else:
            for p in parts:
                result = getattr(result, p)
            return result
