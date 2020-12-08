from dataclasses import dataclass
import itertools


@dataclass
class Envelope:
    levels: object
    times: object
    length: int = None
    loops: int = -1
    reverse: bool = False
    switch: bool = False
    mult: float = 1
    offset: float = 0

    def segments(self):
        for i in itertools.count():
            pass
