from .config import parse_args
from .function import FunctionCall
from .function import separate_commands
from .util import error
import sys


def main(args=None):
    args = parse_args(args)
    commands = separate_commands(args.commands)

    for function, sources in commands:
        commands.append(FunctionCall(function))

    errors = []
    if errors:
        error(*errors, sep='\n')
        return 1


if __name__ == '__main__':
    sys.exit(main())
