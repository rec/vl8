from . import to_section
from pathlib import Path
import json
import toml
import yaml

READERS = {'.json': json, '.toml': toml, '.yaml': yaml}


def load(filename):
    p = Path(filename)
    try:
        reader = READERS[p.suffix]
    except KeyError:
        raise ValueError('Cannot understand suffixs', p.suffix)
    with p.open() as fp:
        return reader.load(fp)


def merge(configs, overwrite=True):
    result = {}
    for cfg in configs:
        for name, section in cfg.items():
            rsection = result.setdefault(to_section(name), {})

            for k, v in section.items():
                if overwrite or k not in rsection:
                    rsection[k] = v
                    continue

                rv = rsection[k]
                if isinstance(rv, dict):
                    rv.update(v)
                elif isinstance(rv, list):
                    rv += v
                else:
                    raise TypeError(str(type(rv)))

    return result
