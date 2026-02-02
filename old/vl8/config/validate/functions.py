import functools
import importlib

NAME = "_name"
ARGS = "_args"


def validate(functions):
    for k, v in functions.items():
        if isinstance(v, str):
            v = {NAME: v}
        elif isinstance(v, list):
            v = {NAME: v[0], ARGS: v[1:]}

        if not isinstance(v, dict):
            yield f"function {k} was not a string or dict" % k
        elif NAME not in v:
            yield f"function {k} had no {NAME}"
        else:
            name = v.pop(NAME)
            args = v.pop(ARGS, [])
            # TODO: this should happen later
            function = _import(name)
            functions[k] = functools.partial(function, *args, **v)


def _import(symbol):
    parts = []
    while True:
        try:
            result = importlib.import_module(symbol)
        except ModuleNotFoundError:
            symbol, *rest = symbol.rsplit(".", maxsplit=1)
            if not rest:
                raise
            parts.insert(0, *rest)
        else:
            for p in parts:
                result = getattr(result, p)
            return result
