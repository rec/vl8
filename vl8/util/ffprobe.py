import subprocess as sp
import xmod

_DURATION = 'Duration: '
_STREAM = 'Stream #0:0: Audio: '


@xmod
def ffprobe(file):
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
            audio, sample_rate, channels, numbers, bitrate = line.split(', ')
            encoding, *data = audio[len(_STREAM) :].split(maxsplit=1)
            sr, hz = sample_rate.split()
            assert hz == 'Hz', out
            result.update(
                encoding=encoding,
                sample_rate=int(sr),
                channels=channels,
                numbers=numbers,
                bitrate=bitrate,
            )
            if data:
                result['encoding_data'] = data[0]

    return result
