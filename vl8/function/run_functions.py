from . import function_calls
from . import separate_commands
from ..dsp import data
import numpy as np


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

        def convert(x):
            if isinstance(x, data.HasData):
                return x
            if isinstance(x, np.ndarray):
                return data.Data(x, items[0].sample_rate)
            raise ValueError(f'Cannot understand {x}')

        result = (convert(x) for x in function(*items))

        if files:
            pool.extend(result)
        else:
            pool[:] = result

    return pool
