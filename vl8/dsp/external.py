from . import DEFAULT_SAMPLE_RATE
from . import io
from .. import util
from dataclasses import dataclass
import subprocess
import tdir

INFILE, OUTFILE = 'i.wav', 'o.wav'


@dataclass
class Flags:
    dash: str

    def flag(self, key, value):
        if value is True:
            value = sep = ''
        elif self.dash == '-':
            sep = ' '
        else:
            sep = '='
        return f'{self.dash}{key}{sep}{value}'

    def __call__(self, **kwargs):
        return ' '.join(self.flag(k, v) for k, v in kwargs.items())


@dataclass
class External:
    command: str
    flags: Flags

    @tdir
    def __call__(self, data, sample_rate=DEFAULT_SAMPLE_RATE, **kwargs):
        options = self.flags(**kwargs)
        cargs = {'options': options, 'infile': INFILE, 'outfile': OUTFILE}
        parts = [c.format(**cargs) for c in self.command.split()]

        io.write(INFILE, data, sample_rate)
        util.log('$', *parts)
        subprocess.check_call(parts)

        out_data, sr2 = io.read(OUTFILE)
        if sr2 != sample_rate:
            util.error(f'Sample rate changed! {sample_rate} -> {sr2}')
        return out_data


ffmpeg = External('ffmpeg {options} -i {infile} {outfile}', Flags('-'))
rubberband = External('rubberband {options} {infile} {outfile}', Flags('--'))
