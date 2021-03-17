from . import function_names
import importlib
import xmod


@xmod
def importer(name, default_module=None):
    """Import a callable item from a name"""
    f, fname = _import(name, default_module)
    if callable(f):
        return f

    # It's a module or something like it.
    stem = _canon(fname.split('.')[-1])

    for k, v in vars(f).items():
        if callable(v) and not k.startswith('_') and _canon(k) == stem:
            return v

    raise ValueError(f'Nothing callable in {name} ({f})')


def _canon(s):
    return s.lower().replace('_', '')


def _import(name, default_module):
    try:
        return importlib.import_module(name), name
    except ImportError:
        pass

    if default_module:
        name = f'{default_module}.{name}'
        try:
            return importlib.import_module(name), name
        except ImportError:
            pass

    if '.' not in name:
        try:
            fname = function_names.get(name)
        except KeyError:
            raise ImportError(
                f'vl8.functions.{name} cannot be found'
            ) from None
        return importlib.import_module(f'vl8.functions.{fname}'), fname

    path, name = name.rsplit('.', maxsplit=1)
    module = importlib.import_module(path)
    try:
        return getattr(module, name), name
    except AttributeError:
        raise ImportError(f'No attribute in {path} named {name}') from None
