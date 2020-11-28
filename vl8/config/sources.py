from . import DEFAULT
from pathlib import Path


def parse(sources):
    if isinstance(sources, list):
        sources = {DEFAULT: sources}

    for k, v in sources.items():
        if not isinstance(v, list):
            yield 'source %s was not a list' % k
        elif not all(isinstance(i, str) for i in v):
            yield 'source %s was not a list of strings' % k
        else:
            sources[k] = [Path(i).expanduser() for i in v]
