from ..util.audio_formats import AUDIO_FORMATS
import xmod


def is_function(x):
    return not ('.' in x and x.split('.')[-1] in AUDIO_FORMATS)


@xmod
def separate_commands(commands, is_function=is_function):
    results = []

    function, args = None, []
    for a in commands or ():
        if is_function(a):
            if function:
                results.append([function, args])
                function, args = None, []
            function = a
        else:
            args.append(a)
    if function or args:
        results.append([function, args])

    return results
