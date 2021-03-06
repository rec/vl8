# from .config import parse_args
# from .util import error
from . import importer
import inspect


class Function:
    def __call__(self, *sources):
        return self.function(*sources)

    def __init__(self, name):
        def signature(s):
            return list(inspect.signature(s).parameter.values())

        f = self.function = importer(name)
        self.sig = signature(f)

        if isinstance(f, type):
            f_call = vars(f).get('__call__')
            if not f_call:
                raise ValueError(f'Class {name} is not callable')

            call = signature(f_call)
            if not call or call[0].name != 'self':
                raise ValueError(f'{f}.__call__ must be a member function')
            if len(call) != 2:
                raise ValueError(f'{f}.__call__() takes one argument')
            call = call[1]
        elif not self.sig:
            raise ValueError(f'{f}() needs at least one argument')
        else:
            call = self.sig.pop(0)

        if call.kind in (call.POSITIONAL_ONLY, call.POSITIONAL_OR_KEYWORD):
            self.simple = True
        elif call.kind is call.VAR_POSITIONAL:
            self.simple = False
        else:
            raise ValueError(f'Bad signature for {f}({self.sig})')


def _split_args(name):
    # import yaml
    # fname, args = _split_args(name)
    # self.config = yaml.safe_load(f'{args}')

    for begin, end in '()', '{}':
        if name.endswith(end):
            if begin not in name:
                raise ValueError(f'"{end}" with no "{begin}" in "{name}"')
            return name[:-1].split(begin, maxsplit=1)

    return name, ''
