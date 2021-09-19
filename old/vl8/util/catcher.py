import contextlib
import functools
import xmod


class Catcher(Exception):
    consume_exception = False

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

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            if isinstance(exc_val, Catcher):
                self.exceptions.extend(exc_val.exceptions)
            else:
                self.exceptions.append(exc_val)

        return self.consume_exception

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


def _map(f, seq):
    catcher = Catcher()
    results = []

    for v in seq:
        with catcher:
            results.append(f(*v))

    catcher.raise_if()
    return results


def map_sequence(f, seq):
    return _map(lambda x: f([x]), seq)


def map_star(f, seq):
    return _map(f, seq)


def map_zip(fseq, seq):
    return _map(lambda f, x: f(x), zip(fseq, seq))


@xmod
@contextlib.contextmanager
def catcher(catcher=None):
    catcher = catcher or Catcher()

    with catcher:
        yield catcher

    catcher.raise_if()
