from .config import parse_args
from .function import FunctionCall
from .util import error
import sys


def main(args=None):
    args = parse_args.parse(args)
    # commands, errors, results = [], [], []
    commands = []

    for function, sources in args.commands:
        commands.append(FunctionCall(function))

    errors = []
    if errors:
        error(*errors, sep='\n')
        return 1


if __name__ == '__main__':
    sys.exit(main())
