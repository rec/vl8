from . import function_calls
from . import separate_commands
from ..dsp import data
import numpy as np

DEFAULT_SAMPLE_RATE = 44100


def run(args):
    # If a function DOES have files, it acts on those files
    # and then adds them to the pool.
    #
    # If the function DOES NOT have files, it replaces the
    # existing pool by acting on it.
    #
    # TODO: new "parentheses" functions `pa` and `ren` create subpools
    # TODO: use `args`
    # TODO: a way to explicitly name results in the pool

    pool = []
    commands = separate_commands(args.commands)

    for function, files in function_calls(commands):
        items = files or pool
        # TODO: config!
        sample_rate = items[0].sample_rate if items else DEFAULT_SAMPLE_RATE
        results = function(*items)
        results = list(results)
        results = _apply(results, sample_rate)
        results = list(results)
        if files:
            pool.extend(results)
        else:
            pool[:] = results

    return pool


def _apply(results, sample_rate):
    if isinstance(results, (data.HasData, np.ndarray)):
        results = [results]

    for x in results:
        if isinstance(x, data.HasData):
            yield x
        elif isinstance(x, np.ndarray):
            yield data.Data(x, sample_rate)
        else:
            raise ValueError(f'Cannot understand {x}')
