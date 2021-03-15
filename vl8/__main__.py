from .config import parse_args
from .function import run_functions
import sys


def main(args=None):
    args = parse_args(args)
    _write_files(run_functions(args))


def _write_files(files):
    pass


if __name__ == '__main__':
    sys.exit(main())
