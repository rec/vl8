import stroll
# import pydub
import runs


def convert():
    for flac in stroll('/data/sorta', suffix='.flac'):
        wav = flac.with_suffix('.wav')
        runs(f'ffmpeg -i "{flac}" "{wav}"')


if __name__ == '__main__':
    convert()
