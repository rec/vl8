from . import sources, functions, tasks, arguments, options


def validate(config):
    # TODO: get stuff from args and validate
    result = {'options': config.pop('options', {})}

    for section in sources, functions, tasks, arguments, options:
        name = section.__name__.split('.')[-1]
        result[name] = config.pop(name, {})
        yield from section.validate(result[name])

    if config:
        yield f'Unknown configuration values {config}'
        config.clear()

    config.update(result)
