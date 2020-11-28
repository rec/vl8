from . import sources, functions, tasks


def parse(config):
    for section in sources, functions, tasks:
        cfg = config.setdefault(section.__name__, {})
        for k, v in cfg.items():
            yield from section.parse(k, v)
