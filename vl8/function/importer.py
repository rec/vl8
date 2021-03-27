from . import function_names
import importlib
import xmod


@xmod
def importer(name, default_module=None):
    try:
        return import_callable(name, default_module or 'vl8.functions')
    except ImportError:
        if default_module or '.' in name:
            raise

    fname = function_names.get(name, None)
    if not fname:
        raise ImportError(f'vl8.functions.{name} cannot be found')

    mod = importlib.import_module(f'vl8.functions.{fname}')
    return _make_callable(mod, fname)


def import_callable(name, default_module=None):
    """Import a callable item from a name"""
    f = _import(name)
    if not f and default_module:
        f = _import(f'{default_module}.{name}')

    if not f:
        raise ModuleNotFoundError(f"No module named '{name}'")

    return _make_callable(f, name)


def _make_callable(f, name):
    if callable(f):
        return f

    # It's a module or something like it.
    stem = _canon(name.split('.')[-1])

    for k, v in vars(f).items():
        if callable(v) and not k.startswith('_') and _canon(k) == stem:
            return v

    raise ImportError(f'Nothing callable in {name}')


def _canon(s):
    return s.lower().replace('_', '')


def _import(name):
    try:
        return importlib.import_module(name)
    except ImportError:
        pass

    # Maybe it's path.to.module.attribute
    mod_path, *attr = name.rsplit('.', maxsplit=1)
    if not attr:
        return

    try:
        module = importlib.import_module(mod_path)
    except ImportError:
        return
    else:
        return getattr(module, attr[0], None)
