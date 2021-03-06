from . import sources, functions, tasks, arguments, options

NAMED_SECTIONS = {
    'sources': sources,
    'functions': functions,
    'tasks': tasks,
    'arguments': arguments,
    'options': options,
}


def validate(config):
    # TODO: get stuff from args and validate
    result = {'options': config.pop('options', {})}

    for name, section in NAMED_SECTIONS.items():
        result[name] = config.pop(name, {})
        yield from section.validate(result[name])

    if config:
        yield f'Unknown configuration values {config}'
        config.clear()

    config.update(result)
