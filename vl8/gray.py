import graycode
import itertools


def iterate(start=0, forward=True):
    for i in itertools.count(start):
        if forward:
            yield graycode.tc_to_gray_code(i)
        else:
            yield graycode.gray_code_to_tc(i)
