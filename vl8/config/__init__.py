# These are the three top sections in a config file dictionary.
SOURCES = 'sources'
FUNCTIONS = 'functions'
TASKS = 'tasks'
OPTIONS = 'options'

SECTIONS = SOURCES, FUNCTIONS, TASKS, OPTIONS

# These are special fields for functions and tasks that allow you
# to load and call Python functions
NAME = '_name'
ARGS = '_args'
DEFAULT = '_'


def to_section(x):
    return _find_unique(x, SECTIONS, 'section')


def _find_unique(x, items, name):
    # Expand shorthand names
    if x:
        for s in items:
            if s.startswith(x):
                return s

    raise ValueError(f'Do not understand {name} "{x}"')
