from pathlib import Path
from vl8.dsp import io


def assert_files_equal(filename, result, sample_rate):
    io.write(filename, result, sample_rate=sample_rate)
    rfile = Path(__file__).parent / 'dsp/results' / filename
    d1, d2 = Path(filename).read_bytes(), rfile.read_bytes()
    assert len(d1) == len(d2), f'{len(d1)} == {len(d2)}'
    assert d1 == d2
