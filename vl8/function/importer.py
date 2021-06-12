from pathlib import Path
import importlib
import xmod

DEFAULT_MODULES = '', 'vl8.functions.', 'vl8.functions.gen.'


@xmod
def importer(name):
    for d in DEFAULT_MODULES:
        mod = _import(d, name)
        if mod:
            return _make_callable(*mod)

    raise ImportError(f'{name} can\'t be found anywhere: {DEFAULT_MODULES}')


def _import(d, path):
    if d and path and '.' not in path:
        # Expand single-word names
        mod = importlib.import_module(d[:-1])
        parent = Path(mod.__file__).parent
        pyfiles = [p.stem for p in parent.iterdir() if p.suffix == '.py']
        if path not in pyfiles:
            stems = [f for f in pyfiles if f.startswith(path)]
            if not stems:
                return
            if len(stems) > 1:
                raise ImportError(f'Ambiguous import {path}')
            path = stems[0]

        return importlib.import_module(d + path), path

    attributes = []
    name = path
    while True:
        try:
            mod = importlib.import_module(name)

        except ImportError:
            *first, last = name.rsplit('.', maxsplit=1)
            if not first:
                return
            attributes.insert(0, last)
            name = first[0]

        else:
            if not attributes:
                return mod, name

            for a in attributes:
                try:
                    mod = getattr(mod, a)
                except AttributeError:
                    break
            else:
                return mod, a
            break


def _make_callable(f, name):
    if callable(f):
        return f

    def canon(s):
        return s.lower().replace('_', '')

    # It's a module or something like it.
    stem = canon(name.split('.')[-1])

    v = vars(f)
    try:
        return v[stem]
    except KeyError:
        pass

    for k, v in vars(f).items():
        if callable(v) and not k.startswith('_') and canon(k) == stem:
            return v

    raise ImportError(f'Nothing callable in {name}')
