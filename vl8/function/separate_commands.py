from ..util.audio_formats import AUDIO_FORMATS
import xmod


def is_function(x):
    if '.' in x:
        suffix = x.rsplit('.', maxsplit=1)[-1]
        return suffix.upper() not in AUDIO_FORMATS
    return True


@xmod(mutable=True)
def separate_commands(commands):
    function, args = None, []
    for a in commands or ():
        if is_function(a):
            if function:
                yield function, args
                function, args = None, []
            function = a
        else:
            args.append(a)
    if function or args:
        yield function, args
