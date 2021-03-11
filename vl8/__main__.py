from .config import parse_args
from .dsp.file import File
from .function import FunctionCall
from .function import separate_commands
from .util import catcher
import sys


def main(args=None):
    args = parse_args(args)
    commands = separate_commands(args.commands)

    function_calls = []
    with catcher() as cat:
        for function, files in commands:
            with cat:
                function = FunctionCall(function)

            new_files = []
            for file in files:
                with cat:
                    new_files.append(File(file))

            function_calls.append((function, new_files))

    return function_calls


if __name__ == '__main__':
    sys.exit(main())
