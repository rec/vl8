from pathlib import Path

from old.vl8.dsp import io

WRITE_RESULTS = False


def assert_files_equal(filename, result, sample_rate, write_results=WRITE_RESULTS):
    io.write(filename, result, sample_rate=sample_rate)
    if write_results:
        io.write(results_file(filename), result, sample_rate=sample_rate)

    assert_equal(filename)


def results_file(filename):
    return Path(__file__).parent / "dsp/results" / filename


def assert_equal(filename):
    d1 = Path(filename).read_bytes()
    d2 = results_file(filename).read_bytes()
    assert len(d1) == len(d2), f"{len(d1)} == {len(d2)}"
    assert d1 == d2
