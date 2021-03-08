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


def map_dict(f, args):
    catcher = Catcher()
    result = {}

    for k, v in args.items():
        with catcher:
            k, v = f(k, v)
            if k in result:
                raise KeyError(k, 'Duplicate key')
            result[k] = v
    catcher.raise_if()
    return result


def map_list(f, *values):
    catcher = Catcher()
    result = []

    for v in values:
        with catcher:
            result.append(f(v))
    catcher.raise_if()
    return result
