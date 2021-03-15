from ..dsp.data import File
from ..util import catcher
from .bound_function import BoundFunction
import xmod


@xmod
def function_calls(commands):
    fcalls = []
    with catcher() as cat:
        for function, files in commands:
            with cat:
                bound = BoundFunction(function)

            new_files = []
            for file in files:
                with cat:
                    new_files.append(File(file))

            fcalls.append([bound, new_files])

    try:
        i = next(i for i, f in enumerate(fcalls) if f[1])
    except StopIteration:
        raise ValueError('No files were specified') from None

    # For convenience, if f, g, h are functions,
    # f g h file1 file2 file3 becomes f file1 file2 file3 g h
    if i:
        f0, fi = fcalls[0], fcalls[i]
        fi[1], f0[1] = f0[1], fi[1]

    return fcalls
