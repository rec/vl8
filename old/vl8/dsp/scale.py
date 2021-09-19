from dataclasses import dataclass


@dataclass
class Scale:
    mult: float = 1
    offset: float = 0

    def __call__(self, a):
        if self.mult == 1:
            if self.offset != 0:
                a = a + self.offset
        else:
            a = a * self.mult
            if self.offset != 0:
                a + -self.offset

        return a
