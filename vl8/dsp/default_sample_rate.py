from typing import Optional
import xmod

DEFAULT_DEFAULT = 44100
_DEFAULT = None


@xmod
def get(default: Optional[int] = None):
    return default or _DEFAULT or DEFAULT_DEFAULT


def set(default):
    global _DEFAULT
    _DEFAULT = default
