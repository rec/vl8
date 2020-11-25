# import pydub
import runs
import stroll


def convert():
    for flac in stroll('/data/vl8', suffix='.flac'):
        wav = flac.with_suffix('.wav')
        runs(f'ffmpeg -i "{flac}" "{wav}"')


if __name__ == '__main__':
    convert()
