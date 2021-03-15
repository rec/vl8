from . import function
from .config import parse_args
from .dsp import io
import sys


def main(args=None):
    pa = parse_args(args)
    data = function.run(pa)
    for f in io.write_data(data, pa.out_file, pa.out_format, pa.dtype):
        print('Written', f)


if __name__ == '__main__':
    sys.exit(main())
