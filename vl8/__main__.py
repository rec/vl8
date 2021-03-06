from .config import parse_args
from .util import error
from .util.function import Function
import sys


def main(args=None):
    args = parse_args.parse(args)
    # commands, errors, results = [], [], []
    commands = []

    for function, sources in args.commands:
        commands.append(Function(function))

    errors = []
    if errors:
        error(*errors, sep='\n')
        return 1


if __name__ == '__main__':
    sys.exit(main())
