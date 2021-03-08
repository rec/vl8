import functools


class Catcher(Exception):
    def __init__(self):
        self.exceptions = []

    def __bool__(self):
        return bool(self.exceptions)

    def decorate(self, fn):
        @functools.wrapper(fn)
        def wrapped(*args, **kwargs):
            with self:
                return fn(*args, **kwargs)

        return wrapped

    def map(self, f, *values):
        results = []
        for v in values:
            with self:
                results.append(f(v))
        self.raise_if()
        return results

    def __enter__(self):
        pass

    def __exit__(self, *args):
        if args[0]:
            self.exceptions.append(args)

        return True

    def __str__(self):
        if not self.exceptions:
            return ''
        if len(self.exceptions) == 1:
            return str(self.exceptions[0])
        # TODO: clean up!
        return str(self.exceptions)

    def raise_if(self):
        if self:
            raise self
