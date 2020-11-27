from . import SOURCES, FUNCTIONS, TASKS
from . import sources, functions, tasks


def parse(config):
    yield from sources.parse(config.setdefault(SOURCES, {}))
    yield from functions.parse(config.setdefault(FUNCTIONS, {}))
    yield from tasks.parse(config.setdefault(TASKS, {}))
