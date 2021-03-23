from ..util import abbrev
from pathlib import Path

_FUNCTIONS = None
FUNCTIONS_DIR = Path(__file__).parents[1]


def names():
    global _FUNCTIONS
    if _FUNCTIONS is None:
        d = FUNCTIONS_DIR / 'functions'
        files = (i.stem for i in d.iterdir() if i.suffix == '.py')
        _FUNCTIONS = {i: i for i in files if not i.startswith('_')}

    return _FUNCTIONS


def get(fname):
    return abbrev(names(), fname)
