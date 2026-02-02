import argparse
import xmod


@xmod
def parse_args(args=None):
    return _PARSER.parse_args(args)


def _parser():
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument("commands", nargs="+", help=_COMMANDS_H)
    p.add_argument("--calc-type", "-a", default="float32", help=_CALC_TYPE_H)
    p.add_argument("--continue", "-c", action="store_true", help=_CONTINUE_H)
    p.add_argument("--dry-run", "-d", action="store_true", help=_DRY_RUN_H)
    p.add_argument("--force", "-f", action="store_true", help=_FORCE_H)
    p.add_argument("--out-file", "-o", default="", help=_OUT_H)
    p.add_argument("--out-format", "-r", default=".wav", help=_FORMAT_H)
    p.add_argument("--out-type", "-t", default="int16", help=_OUT_TYPE_H)
    p.add_argument("--verbose", "-v", action="store_true", help=_VERBOSE_H)

    return p


_DESCRIPTION = """slice, dice, mix-and-match"""
_CALC_TYPE_H = """What datatype to perform calculations in"""
_COMMANDS_H = "A list of commands and files to run"
_CONTINUE_H = "Try to continue to processing after an error has occurred"
_DRY_RUN_H = "Check that files and functions exist but do not run"
_FORCE_H = """Overwrite existing files"""
_OUT_H = """File or file pattern to output to"""
_OUT_TYPE_H = """What datatype to output to"""
_FORMAT_H = """Default file format for out"""
_VERBOSE_H = """Print more stuff"""

_PARSER = _parser()
DEFAULTS = vars(parse_args([""]))
DEFAULTS.pop("commands")
