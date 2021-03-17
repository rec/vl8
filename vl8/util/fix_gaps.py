from . import error
from typing import List, Union, Optional
import math
import xmod

Number = Union[int, float]


@xmod
def fix_gaps(
    durations: List[int],
    gaps: Union[Number, List[Number]],
    pre: float = 0,
    post: float = 0,
    sample_rate: Optional[int] = None,
):
    if pre < 0 or post < 0:
        raise ValueError('pre and post cannot be negative')

    if not isinstance(gaps, list):
        gaps = [gaps]
    elif not gaps:
        raise ValueError('gap must be a non-empty list or an integer')

    n = len(durations)
    scale = math.ceil(n / len(gaps))
    gaps = [pre] + (gaps * scale)[: n - 1] + [post]

    if sample_rate:
        gaps = [g * sample_rate for g in gaps]

    gaps = [round(g) for g in gaps]

    # Fix any fade gaps that are too long.
    for i, gap in enumerate(gaps):
        if i > 0:
            gap = max(gap, -durations[i - 1])
        if i < n:
            gap = max(gap, -durations[i])
        if gaps[i] != gap:
            error(f'Gap {i}: {gap} was longer than the sample!')
            gaps[i] = gap

    assert len(gaps) == n + 1
    return gaps
