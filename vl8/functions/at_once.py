import numpy as np


def at_once(samples, dtype, overlap=0.5):
    max_length = max(len(s) for s in samples)
    min_length = min(len(s) for s in samples)

    begin = round(overlap * (max_length - min_length) / 2)
    if begin < 0:
        offset = -begin
        length = max_length + offset
    else:
        offset = 0
        length = max(max_length, begin + min_length)

    channels = max(s.channels for s in samples)
    result = np.zeros((channels, length), dtype)

    for s in samples:
        begin = offset + round(overlap * (max_length - len(s)) / 2)
        result[:, begin : begin + len(s)] += s

    return result
