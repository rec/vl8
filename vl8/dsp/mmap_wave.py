from .. import util
from struct import unpack_from, calcsize
import numpy as np

# See http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html

WAVE_FORMAT_PCM = 0x0001
WAVE_FORMAT_IEEE_FLOAT = 0x0003
WAVE_FORMATS = {WAVE_FORMAT_PCM, WAVE_FORMAT_IEEE_FLOAT}

HEADER_LENGTH = 8
FMT_FORMAT = '<HHIIHH'
FMT_LENGTH = calcsize(FMT_FORMAT)
assert FMT_LENGTH == 16

FMT_BLOCK_LENGTHS = {16, 18, 40}

PCM_BITS_PER_SAMPLE = {8, 16, 32, 64}
FLOAT_BITS_PER_SAMPLE = {32, 64}

BITS_PER_SAMPLE = PCM_BITS_PER_SAMPLE, FLOAT_BITS_PER_SAMPLE

# Making 24 bits work transparently is probably impossible:
# https://stackoverflow.com/a/34128171/43839


class MmapWave(np.memmap):
    def __new__(cls, filename, mode='r', order='C', always_2d=False):
        begin, end, fmt = _metadata(filename)

        (
            wFormatTag,
            nChannels,
            nSamplesPerSec,
            nAvgBytesPerSec,
            nBlockAlign,
            wBitsPerSample,
        ) = unpack_from(FMT_FORMAT, fmt[:FMT_LENGTH])

        if wFormatTag not in WAVE_FORMATS:
            raise ValueError(f'Do not understand wFormatTag={wFormatTag}')

        is_float = wFormatTag == WAVE_FORMAT_IEEE_FLOAT
        if wBitsPerSample not in BITS_PER_SAMPLE[is_float]:
            raise ValueError(f'Cannot mmap wBitsPerSample={wBitsPerSample}')

        type_name = ('int', 'float')[is_float]
        dtype = f'{type_name}{wBitsPerSample}'

        bytes_per_frame = wBitsPerSample // 8 * nChannels

        extra = (end - begin) % bytes_per_frame
        if extra:
            util.error(f'Extra bytes {extra}')

        frame_length = (end - begin) // bytes_per_frame

        if nChannels == 1 and not always_2d:
            shape = (frame_length,)
        elif order == 'C':
            shape = frame_length, nChannels
        elif order == 'F':
            shape = nChannels, frame_length
        else:
            raise ValueError(f'Bad order "{order}"')

        self = np.memmap.__new__(
            cls, filename, dtype, mode, begin, shape, order
        )

        self.sample_rate = nSamplesPerSec
        self.order = order
        self.channnels = nChannels

        return self

    @property
    def length(self):
        return self.shape[self.ndim > 1 and self.order != 'C']

    @property
    def duration(self):
        return self.length / self.sample_rate


def _metadata(filename):
    begin = end = fmt = None

    with open(filename, 'rb') as fp:
        (tag, _, _), *chunks = _chunks(fp)
        if tag != b'WAVE':
            raise ValueError(f'Not a WAVE file: {tag}')

        for tag, b, e in chunks:
            if tag == b'fmt ':
                if not fmt:
                    b += HEADER_LENGTH
                    fp.seek(b)
                    fmt = fp.read(e - b)
                else:
                    util.error('fmt chunk after first ignored')
            elif tag == b'data':
                if not (begin or end):
                    begin, end = b, e
                else:
                    util.error('data chunk after first ignored')

    if begin is None:
        raise ValueError('No data chunk found')

    if fmt is None:
        raise ValueError('No fmt chunk found')

    if len(fmt) not in FMT_BLOCK_LENGTHS:
        raise ValueError('Weird fmt block')

    if len(fmt) == 40:
        raise ValueError('Cannot read extensible format WAV files')

    return begin, end, fmt


def _chunks(fp):
    file_size = fp.seek(-1, 2)
    fp.seek(0)

    def read_one(format):
        return unpack_from('<' + format, fp.read(calcsize(format)))[0]

    def read_tag():
        tag = read_one('4s')
        if tag and not tag.rstrip().isalnum():
            util.error(f'Dubious tag {tag}')
        return tag

    def read_int():
        return read_one('I')

    tag = read_tag()
    if tag != b'RIFF':
        raise ValueError(f'Not a RIFF file: {tag}')

    size = read_int()
    yield read_tag(), 0, size

    while fp.tell() < file_size:
        begin = fp.tell()
        tag, chunk_size = read_tag(), read_int()
        fp.seek(chunk_size, 1)
        end = fp.tell()
        if end > file_size:
            util.error(f'Incomplete chunk: {end} > {file_size}')
            end = file_size
        yield tag, begin, end


if __name__ == '__main__':
    import sys

    for i in sys.argv[1:]:
        mw = MmapWave(i)
        print(mw.shape)
        print(mw.length)
        print(mw.duration)
        print(mw)

    print('done')
