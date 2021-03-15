from . import function_calls
from . import separate_commands
import xmod


def _run_calls(function_calls, args):
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

    while function_calls:
        function, files = function_calls.pop(0)
        if files:
            pool.extend(function(*files))
        else:
            pool[:] = function(*pool)

    return pool


@xmod
def run_functions(args):
    commands = separate_commands(args.commands)
    fcalls = function_calls(commands)
    return _run_calls(fcalls, args)
