from . import function_calls
from . import separate_commands


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
        if files:
            pool.extend(function(*files))
        else:
            pool[:] = function(*pool)

    return pool
