# These are the three top sections in a config file dictionary.
SOURCES = 'sources'
FUNCTIONS = 'functions'
TASKS = 'tasks'

SECTIONS = SOURCES, FUNCTIONS, TASKS

# These are special fields for functions and tasks that allow you
# to load and call Python functions
NAME = '_name'
ARGS = '_args'


def to_section(x):
    # Expand shorthand names
    if x:
        for s in SECTIONS:
            if s.startswith(x):
                return s

    raise ValueError('Do not understand section "%s"' % x)
