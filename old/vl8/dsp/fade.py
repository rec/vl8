import numpy as np
import xmod


@xmod
def fade(src: np.ndarray, fade_in: np.ndarray, fade_out: np.ndarray) -> None:
    if not src.size:
        return

    # TODO: unsafe leaves the possibility of overs in a fixed-point format.
    def mul(x, y):
        np.multiply(x, y, out=x, casting="unsafe")

    fi = len(fade_in)
    fo = len(fade_out)

    ratio = (fi + fo) / src.shape[1]
    if ratio and ratio > 1:
        fi = round(fi / ratio)
        fo = src.shape[1] - fi

    if fi:
        mul(src[:, :fi], fade_in[:fi])

    if fo:
        mul(src[:, -fo:], fade_out[-fo:])
