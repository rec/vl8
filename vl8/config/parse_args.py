import argparse
import xmod


@xmod
def parse_args(args=None):
    return _PARSER.parse_args(args)


def _parser():
    p = argparse.ArgumentParser(description='slice, dice, mix-and-match')

    p.add_argument(
        'commands', nargs='+', help='A list of commands and files to run'
    )
    p.add_argument(
        '--numbers', default='float32',
        help='What datatype to perform calculations in'
    )
    p.add_argument(
        '--sample-rate', '-s', type=int,
        help='Set or override the given sample rate'
    )
    p.add_argument(
        '--normalize', '-n', help='Normalize the output before writing'
    )
    p.add_argument(
        '--gain', '-g', help='Change gain: as a ratio, or in + or - db'
    )
    p.add_argument(
        '--continue', '-c', action='store_true',
        help='Try to continue to processing after an error has occurred'
    )
    p.add_argument(
        '--dry-run', '-d', action='store_true',
        help='Check that files and functions exist but do not run'
    )
    p.add_argument(
        '--force', '-f', action='store_true', help='Overwrite existing files'
    )
    p.add_argument(
        '--fade', type=float, default=0.2,
        help='Time in seconds for fades at begin and end'
    )
    p.add_argument(
        '--output', '-o', default='', help='File or file pattern to output to'
    )
    p.add_argument(
        '--format', default='.wav', help='What datatype to output to'
    )
    p.add_argument(
        '--type', '-t', default='int16', help='Default file format for out'
    )
    p.add_argument(
        '--verbose', '-v', action='store_true', help='Print more stuff'
    )

    return p


_PARSER = _parser()
DEFAULTS = vars(parse_args(['']))
DEFAULTS.pop('commands')
