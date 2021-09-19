import numpy as np

# Operations on floating point samples only


def clean(arr, normalize=False, out=None):
    """Remove DC offsets, and then either unclip or normalize"""
    dc = subtract_dc(arr, out)
    return _level(dc, normalize, dc)


def subtract_dc(arr, out=None):
    """
    Remove any DC offsets on the channels.
    Might result in samples with absolute values greater than 1.
    """
    mean = np.mean(arr, axis=0)
    return np.subtract(arr, mean, out)


def normalize(arr, out=None):
    _level(arr, True, out)


def unclip(arr, out=None):
    _level(arr, False, out)


def _level(arr, normalize, out):
    level = max(np.amax(arr), -np.amin(arr))
    if not level or (not normalize and level <= 1):
        return arr

    return arr.divide(arr, level, out)
