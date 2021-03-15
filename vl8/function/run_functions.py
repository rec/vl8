from . import function_calls
from . import separate_commands


def _run_calls(fcalls, args):
    # If a function DOES have files, it acts on those files
    # and then adds them to the pool.
    #
    # If the function DOES NOT have files, it replaces the
    # existing pool by acting on it.
    #
    # TODO: new "parentheses" functions `pa` and `ren` create subpools
    # TODO: use `args`
    # TODO: a way to explicitly name results in the pool
    #
    pool = []

    for function, files in fcalls:
        if files:
            pool.extend(function(*files))
        else:
            pool[:] = function(*pool)

    return pool


def run(args):
    commands = separate_commands(args.commands)
    fcalls = function_calls(commands)
    return _run_calls(fcalls, args)
