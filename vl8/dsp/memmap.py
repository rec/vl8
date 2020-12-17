from .. import util
import numpy as np
import struct

ERROR = 'Not in .WAV format'

INTRO = '<4sI'
RIFF = '<4sI4s'
FMT = '<4sHHIIHHHHI16s'
INTRO_SIZE = struct.calcsize(INTRO)
assert INTRO_SIZE == 8
assert struct.calcsize(RIFF) == 12


def _chunks(mm):
    begin = 0
    while begin < len(mm):
        intro = begin + INTRO_SIZE
        tag, chunk_size = struct.unpack_from(INTRO, mm[begin:intro])
        end = intro + chunk_size
        if end > len(mm):
            util.error(f'Chunk overrun in {tag}: {end} > {len(mm)}')

        yield tag, mm[intro:end]
        begin = end if begin else 12


def wave(filename, mode='r'):
    mm = np.memmap(filename, mode=mode)
    # wave_size = None

    chunks = (f'{t}: {len(c)}' for t, c in _chunks(mm))
    print(*chunks, sep='\n')


if __name__ == '__main__':
    import sys

    for i in sys.argv[1:]:
        wave(i)

    print('done')


"""
    for tag, begin, end in chunks(mm):
        if wave_size is None:
            assert tag == 'RIFF'
            wave_size = len(segment)

            assert

    with open(filename, 'rb') as fp:
        with mmap.mmap(fp.fileno(), 0) as mm:

            size = struct.calcsize(format)
            data = fp.read(size)
            return struct.unpack_from(format, data)

        ckID, cksize1, WAVEID = _read(RIFF)

        if not (ckID == 'RIFF' and WAVEID == 'WAVE'):
            raise ValueError(ERROR)

        (
            ckID,
            cksize2,
            wFormatTag,
            nChannels,
            nSamplesPerSec,
            nAvgBytesPerSec,
            nBlockAlign,
            wBitsPerSample,
            cbSize,
            wValidBitsPerSample,
            dwChannelMask,
            SubFormat,
        ) = _read(FMT)

        if ckID != 'fmt ':
            raise ValueError(ERROR)
"""
