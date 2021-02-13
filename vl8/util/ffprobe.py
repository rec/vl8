from fractions import Fraction
import subprocess as sp
import xmod

_DURATION = 'Duration: '
_STREAM = 'Stream #0:0: Audio: '


@xmod
def ffprobe(file):
    with open(file):
        pass

    cmd = ('ffprobe', '-hide_banner', file)
    out = sp.check_output(cmd, encoding='utf8', stderr=sp.STDOUT)

    result = {}
    for line in out.splitlines():
        line = line.strip()
        if line.startswith(_DURATION):
            for i in line.split(', '):
                name, value = i.split(': ', maxsplit=1)
                result[name.lower()] = value
        elif line.startswith(_STREAM):
            names = 'audio', 'sample_rate', 'channels', 'numbers', 'bitrate'
            result.update(zip(names, line.split(', ')))

    return {k: _clean(k, v) for k, v in result.items()}


def _clean(key, value):
    if key == 'bitrate':
        br, speed = value.split()
        assert speed == 'kb/s', value
        return 1000 * int(br)

    elif key == 'channels':
        v = value.split()[0]
        if v == 'mono':
            return 1
        if v == 'stereo':
            return 2
        if v.isnumeric():
            return int(v)

        # Could be "4.0", sigh
        f, *r = v.split('.')
        if r and f.isnumeric() and r[0].isnumeric() and not int(r[0]):
            return int(f)

    elif key == 'duration':
        assert value[2::3] == '::.'
        hours = int(value[0:2])
        minutes = int(value[3:5])
        seconds = Fraction(value[6:])
        return seconds + 60 * (minutes + 60 * hours)

    elif key == 'encoding':
        return value.split()[0]

    elif key == 'numbers':
        return value

    elif key == 'sample_rate':
        sr, hz = value.split()
        assert hz == 'Hz', value
        return int(sr)

    elif key == 'audio':
        assert value.startswith(_STREAM), value
        return value[len(_STREAM) :].split()[0]

    raise ValueError(f'Cannot understand {key}={value}')
