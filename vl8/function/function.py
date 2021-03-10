from . import importer
import inspect

DEFAULT = 'cat'


class Function:
    def __init__(self, name):
        def params(s):
            return dict(inspect.signature(s).parameters)

        self.name = name or DEFAULT
        self.function = importer(name)
        self.params = params(self.function)
        self.is_class = isinstance(self.function, type)

        if not self.is_class:
            # It's a function
            if not self.params:
                raise ValueError(
                    f'{self.function}() needs at least one argument'
                )
            pname = next(iter(self.params))
            param = self.params.pop(pname)

        else:
            f_call = vars(self.function).get('__call__')
            if not f_call:
                raise ValueError(f'Class {name} is not callable')

            call_params = list(params(f_call).values())

            if not call_params or call_params[0].name != 'self':
                raise ValueError(
                    f'{self.function}.__call__() must be a member function'
                )
            if len(call_params) != 2:
                raise ValueError(
                    f'{self.function}.__call__() takes one argument'
                )
            param = call_params[1]

        if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
            self.is_simple = True
        elif param.kind is param.VAR_POSITIONAL:
            self.is_simple = False
        else:
            raise ValueError(
                f'Bad signature for {self.function}({self.params})'
            )

    def required(self):
        return [p.name for p in self.params.values() if p.default is p.empty]

    def __call__(self, *sources, **kwargs):
        if self.is_simple and len(sources) != 1:
            raise TypeError(f'{self.name} takes exactly one argument')
        if self.is_class:
            return self.function(**kwargs)(*sources)
        else:
            return self.function(*sources, **kwargs)
