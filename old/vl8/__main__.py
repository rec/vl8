from . import function
from .config import parse_args
from .dsp import io
import sys


def main(args=None):
    a = parse_args(args)
    data = function.run(a)
    for f in io.write_data(data, a.out_file, a.out_format, a.out_type):
        print('Written', f)


if __name__ == '__main__':
    sys.exit(main())
