from . import abbrev
from ..util import catcher
from .function import Function
import typeguard
import yaml


class FunctionCall:
    def __init__(self, func, **kwargs):
        self.func, self.args = _func_args(func)
        if kwargs:
            self.args.update(_expand(self.func, kwargs))
        params = self.func.params
        required = {p.name for p in params.values() if p.default is p.empty}
        self.missing = required.difference(self.args)

    @property
    def is_simple(self):
        return self.func.is_simple

    def __call__(self, *src):
        if self.missing:
            raise TypeError(f'Missing required arguments {self.missing}')
        return self.func(*src, **self.args)


def _func_args(func):
    if isinstance(func, Function):
        return func, {}
    if isinstance(func, FunctionCall):
        return func.func, dict(func.args)
    if not isinstance(func, str):
        raise TypeError(f'Cannot understand func={func}')

    fname, arg_str = _split_args(func)
    args = yaml.safe_load('{%s}' % arg_str)
    f = Function(fname)
    return f, _expand(f, args)


def _split_args(name):
    for begin, end in '()', '{}':
        if name.endswith(end):
            if begin not in name:
                raise ValueError(f'"{end}" with no "{begin}" in "{name}"')
            return name[:-1].split(begin, maxsplit=1)

    return name, ''


def _expand(func, args):
    def make(key, value):
        param = abbrev(func.params, key)
        if key == param.name:
            argname = key
        else:
            argname = f'{key}/{param.name}'
        typeguard.check_type(argname, value, param)
        return param.name, value

    return catcher.map_dict(make, args)
