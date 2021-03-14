from .config import parse_args
from .dsp.data import File
from .function import BoundFunction
from .function import separate_commands
from .util import catcher
import sys

# An fcall is a function call on a file.


def main(args=None):
    args = parse_args(args)
    commands = separate_commands(args.commands)
    fcalls = _fcalls(commands)
    pool = _run_functions(fcalls)
    _write_pool(pool)


def _write_pool(pool):
    pass


def _fcalls(commands):
    fcalls = []
    with catcher() as cat:
        for function, files in commands:
            with cat:
                function = BoundFunction(function)

            new_files = []
            for file in files:
                with cat:
                    new_files.append(File(file))

            fcalls.append([function, new_files])

    # For convenience, if f, g, h are functions,
    #
    #    f g h file1 file2 file3
    #
    # means the same as
    #
    #    f file1 file2 file3 g h
    try:
        i = next(i for i, f in enumerate(fcalls) if f[1])
    except StopIteration:
        raise ValueError('No files were specified') from None

    if i:
        f0, fi = fcalls[0], fcalls[i]
        fi[1], f0[1] = f0[1], fi[1]

    return fcalls


def _run_functions(fcalls):
    # If a function DOES have arguments, it acts on those files
    # and then adds them to the pool.
    #
    # If the function DOES NOT have arguments, it replaces the
    # existing pool by acting on it.
    #
    # TODO: new "parentheses" functions `pa` and `ren` create subpools
    # TODO: a way to explicitly name results in the pool
    #
    pool = []

    while fcalls:
        function, files = fcalls.pop(0)
        if files:
            pool.extend(function(*files))
        else:
            pool[:] = function(*pool)

    return pool


if __name__ == '__main__':
    sys.exit(main())
