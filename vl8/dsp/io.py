from . import pydub_io
from . import soundfile_io

if True:
    read = pydub_io.read
    write = pydub_io.write
else:
    read = soundfile_io.read
    write = soundfile_io.write
