from fractions import Fraction
import abbrev
import re


def split(n, sample_rate=0):
    match = _match_units(n.strip())
    if not match:
        raise ValueError(f'Bad number "{n}"')
    value, unit = match.groups()

    try:
        u = abbrev(_UNITS, unit)
    except KeyError:
        raise ValueError(f'Unknown unit "{unit}"') from None

    if u:
        return value, 1 / u
    if sample_rate:
        return value, sample_rate
    raise ValueError('No sample rate for "{n}"')


_match_units = re.compile(r"^([^a-zA-Z]*)([a-zA-Z]*)$").match

_MS = Fraction(1, 1000)
_US = _MS / 1000
_NS = _US / 1000

_UNITS = {
    "": Fraction(1),
    "s": Fraction(1),
    "seconds": Fraction(1),
    "milliseconds": _MS,
    "mseconds": _MS,
    "microseconds": _US,
    "useconds": _US,
    "µseconds": _US,
    "nanoseconds": _NS,
    "nseconds": _NS,
    "minutes": Fraction(60),
    "hours": Fraction(60 * 60),
    "weeks": Fraction(60 * 60 * 7),
    "years": Fraction(1826211, 5000),
    "samples": Fraction(0),
}
