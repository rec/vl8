from ..util.audio_formats import AUDIO_FORMATS
import argparse


def parser():
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('commands', nargs='?', help=_COMMANDS_H)
    p.add_argument('--continue', '-c', action='store_true', help=_CONTINUE_H)
    p.add_argument('--dry-run', '-d', action='store_true', help=_DRY_RUN_H)
    p.add_argument('--output', '-o', action='store_true', help=_OUTPUT_H)
    p.add_argument('--verbose', '-v', action='store_true', help=_VERBOSE_H)

    return p


def is_function(x):
    return not ('.' in x and x.split('.')[-1] in AUDIO_FORMATS)


def separate_commands(commands, is_function=is_function):
    results = []

    function, args = None, []
    for a in commands or ():
        if is_function(a):
            if function:
                results.append([function, args])
                function, args = None, []
            function = a
        else:
            args.append(a)
    if function or args:
        results.append([function, args])

    return results


def parse(args=None):
    r = PARSER.parse_args(args)
    r.commands = separate_commands(r.commands)

    return r


_DESCRIPTION = """slice, dice, mix-and-match"""
_COMMANDS_H = 'A list of commands to run'
_CONTINUE_H = 'Try to continue to processing after an error has occurred'
_DRY_RUN_H = 'Check that files and functions exist but do not run'
_OUTPUT_H = """File or file pattern to output to"""
_VERBOSE_H = """Print more stuff"""

PARSER = parser()
