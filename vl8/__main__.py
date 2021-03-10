from .config import parse_args
from .dsp.file import File
from .function import FunctionCall
from .function import separate_commands
from .util import catcher
import sys


def main(args=None):
    def fix(*args):
        return catcher.map_zip((FunctionCall, File), args)

    args = parse_args(args)
    commands = separate_commands(args.commands)
    function_calls = catcher.map_star(fix, commands)
    return function_calls


if __name__ == '__main__':
    sys.exit(main())
