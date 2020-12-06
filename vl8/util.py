import numpy as np
import sys

VERBOSE = True


def normalize(buffer):
    buffer /= max(abs(p) for p in (np.amax(buffer), np.amin(buffer)))


def error(*args, **kwds):
    print(*args, **kwds, file=sys.stderr)


def log(*args, **kwds):
    if VERBOSE:
        error(*args, **kwds)
