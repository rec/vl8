from . import sources, functions, tasks


def parse(config):
    result = {'options': config.pop('options', {})}

    for section in sources, functions, tasks:
        name = section.__name__
        cfg = config.pop(name, {})
        for k, v in cfg.items():
            yield from section.parse(k, v)

        result[name] = cfg

    if config:
        yield f'Unknown configuration values {config}'
        config.clear()

    config.update(result)
