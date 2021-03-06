import sys

VERBOSE = True


def error(*args, **kwds):
    print(*args, **kwds, file=sys.stderr)


def log(*args, **kwds):
    if VERBOSE:
        error(*args, **kwds)
