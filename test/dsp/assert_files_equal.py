from pathlib import Path
from vl8.dsp import io


def assert_files_equal(filename, result, sample_rate):
    io.write(filename, result, sample_rate=sample_rate)
    rfile = Path(__file__).parent / 'results' / filename
    d1, d2 = Path(filename).read_bytes(), rfile.read_bytes()
    assert d1 == d2
