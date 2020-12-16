from . import DEFAULT_SAMPLE_RATE
from . import io
from .. import util
from dataclasses import dataclass
import subprocess
import tdir

INFILE, OUTFILE = 'i.wav', 'o.wav'


@dataclass
class External:
    command: str
    dash: str
    sep: str
    run: object = subprocess.run

    @tdir
    def __call__(self, data, sample_rate=DEFAULT_SAMPLE_RATE, **kwargs):
        def flag(key, value):
            if value is True:
                return f'{self.dash}{key}'
            return f'{self.dash}{key}{self.sep}{value}'

        options = ' '.join(flag(k, v) for k, v in kwargs.items())
        cargs = {'options': options, 'infile': INFILE, 'outfile': OUTFILE}

        # Each part gets expanded separately, because filenames might
        # contain spaces or other special characters.
        parts = [c.format(**cargs) for c in self.command.split()]

        io.write(INFILE, data, sample_rate)
        util.log('$', *parts)
        self.run(parts)

        out_data, sr2 = io.read(OUTFILE)
        if sr2 != sample_rate:
            util.error(f'Sample rate changed! {sample_rate} -> {sr2}')

        return out_data
