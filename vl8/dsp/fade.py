import numpy as np
import xmod


@xmod
def fade(src: np.ndarray, fade_in: np.ndarray, fade_out: np.ndarray) -> None:
    # TODO: unsafe leaves the possibility of overs in a fixed-point format.
    def mul(x, y):
        np.multiply(x, y, out=x, casting='unsafe')

    half = src.shape[1] // 2
    fi = min(len(fade_in), half)
    fo = min(len(fade_out), half)

    if fi:
        mul(src[:, :fi], fade_in[:fi])

    if fo:
        mul(src[:, -fo:], fade_out[-fo:])
