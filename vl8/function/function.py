from . import importer
import inspect


class Function:
    def __init__(self, name):
        self.name = name
        f = self.function = importer(name)
        self.params = _params(f)
        self.is_class = isinstance(f, type)

        if self.is_class:
            f_call = vars(f).get('__call__')
            if not f_call:
                raise ValueError(f'Class {name} is not callable')

            params = list(_params(f_call).values())

            if not params or params[0].name != 'self':
                raise ValueError(f'{f}.__call__ must be a member function')

            if len(params) != 2:
                raise ValueError(f'{f}.__call__() takes one argument')

            param = params[1]

        elif not self.params:
            raise ValueError(f'{f}() needs at least one argument')

        else:
            # It's a function
            param = next(iter(self.params.values()))
            self.params.pop(param.name)

        if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
            self.is_simple = True
        elif param.kind is param.VAR_POSITIONAL:
            self.is_simple = False
        else:
            raise ValueError(f'Bad signature for {f}({self.params})')

    def required(self):
        return [p.name for p in self.params.values() if p.default is p.empty]

    def __call__(self, *sources, **kwargs):
        if self.is_simple and len(sources) != 1:
            raise TypeError(f'{self.name} takes exactly one argument')
        if self.is_class:
            return self.function(**kwargs)(*sources)
        else:
            return self.function(*sources, **kwargs)


def _params(s):
    return dict(inspect.signature(s).parameters)
