from ..util import catcher
from .function import Function
import abbrev
import typeguard
import yaml


class BoundFunction:
    def __init__(self, func, args=None):
        self.func, self.args = _func_args(func)
        if args:
            self.args.update(_expand(self.func, args))
        params = self.func.params
        required = {p.name for p in params.values() if p.default is p.empty}
        self.missing = required.difference(self.args)

    def __call__(self, *files):
        def call(*s):
            return self.func(*s, **self.args)

        if self.missing:
            raise TypeError(f"Missing required arguments {self.missing}")

        if self.func.type is Function.Type.SIMPLE:
            yield from (call(s) for s in files)

        elif self.func.type is Function.Type.MULTIPLE:
            yield call(*files)

        else:
            assert self.func.type is Function.Type.GENERATOR
            yield call()

    def __str__(self):
        return f"BoundFunction({self.func}, {self.args})"


def _func_args(func):
    if func is None:
        return Function(None), {}

    if isinstance(func, Function):
        return func, {}

    if isinstance(func, BoundFunction):
        return func.func, dict(func.args)

    if isinstance(func, str):
        fname, arg_str = _split_args(func)
        parts = arg_str.split(",")
        if parts and all("=" in p for p in parts):
            arg_str = ", ".join(p.replace("=", ": ", 1) for p in parts)

        args = yaml.safe_load("{%s}" % arg_str)
        f = Function(fname)
        return f, _expand(f, args)

    raise TypeError(f"Cannot understand func={func}")


def _split_args(name):
    for begin, end in "()", "{}":
        if name.endswith(end):
            if begin not in name:
                raise ValueError(f'"{end}" with no "{begin}" in "{name}"')
            return name[:-1].split(begin, maxsplit=1)

    return name, ""


def _expand(func, args):
    def make(key, value):
        param = abbrev(func.params, key)
        if key == param.name:
            argname = key
        else:
            argname = f"{key}/{param.name}"
        typeguard.check_type(argname, value, param)
        return param.name, value

    return catcher.map_dict(make, args)
