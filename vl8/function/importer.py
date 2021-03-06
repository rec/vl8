import importlib
import xmod


@xmod
def importer(name):
    """Import a callable item from a name"""
    f = _import(name)
    if callable(f):
        return f

    # It's a module or something like it.
    stem = _canon(name.split('.')[-1])

    for k, v in vars(f).items():
        if callable(v) and not k.startswith('_') and _canon(k) == stem:
            return v

    raise ValueError(f'Nothing callable in {name} ({f})')


def _canon(s):
    return s.lower().replace('_', '')


def _import(name):
    name = name if '.' in name else f'vl8.tasks.{name}'
    try:
        return importlib.import_module(name)
    except ImportError:
        pass

    path, name = name.rsplit('.', maxsplit=1)
    module = importlib.import_module(path)
    try:
        return getattr(module, name)
    except AttributeError:
        raise ImportError(f'No attribute in {path} named {name}') from None
