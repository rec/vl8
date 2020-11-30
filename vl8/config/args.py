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
