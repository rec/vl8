"""Non-flag command line arguments"""


def validate(args):
    if isinstance(args, str):
        args = [args]

    return args
