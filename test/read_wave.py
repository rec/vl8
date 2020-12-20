from pathlib import Path
import stroll
import wave


def read():
    for file in stroll(Path(__file__).parent, suffix='.wav'):
        with file.open('rb') as fp:
            print(file, end=' ')
            try:
                with wave.open(fp) as wp:
                    print(wp.getparams())
            except Exception as e:
                print('***', e)


if __name__ == '__main__':
    read()
