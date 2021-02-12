import argparse


def parser():
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('arguments', nargs='?', help=_ARGUMENTS_H)
    p.add_argument('--continue', '-c', action='store_true', help=_CONTINUE_H)
    p.add_argument('--dry-run', '-d', action='store_true', help=_DRY_RUN_H)
    p.add_argument('--verbose', '-v', action='store_true', help=_VERBOSE_H)

    return p


_DESCRIPTION = """slice, dice, mix-and-match"""
_ARGUMENTS_H = 'Files or JSON or Yaml'
_CONTINUE_H = 'Try to continue to processing after an error has occurred'
_DRY_RUN_H = 'Check that files and functions exist but do not run'
_VERBOSE_H = """Print more stuff"""

PARSER = parser()
parse = PARSER.parse_args


def is_function(argument):
    if '.' not in argument or '(' in argument:
        return True
    return not argument.endswith('.wav')  # TODO


def separate_arguments(arguments, is_function=is_function):
    results = []

    function, args = None, []
    for a in arguments:
        if is_function(a):
            if function:
                results.append((function, args))
                function, args = None, []
            function = a
        else:
            args.append(a)
    if function or args:
        results.append((function, args))

    return results
