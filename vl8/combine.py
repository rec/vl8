from . import util


def combine(files, center=0):
    center = max(0, min(1, center))

    biggest, *rest = sorted(files, key=lambda f: -f.shape[1])
    buf = biggest.copy()

    for sub in rest:
        o = round(center * (buf.shape[1] - sub.shape[1]))
        buf[:, o : o + sub.shape[1]] += sub

    util.normalize(buf)
    return buf


if __name__ == '__main__':
    import stroll

    files = [util.read(f) for f in stroll('/data/vl8/source', suffix='.wav')]

    util.write('/data/vl8/results/combine0.wav', combine(files, 0))
    util.write('/data/vl8/results/combine1.wav', combine(files, 1))
    util.write('/data/vl8/results/combine5.wav', combine(files, 0.5))
