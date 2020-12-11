from .. import parse_args


def validate(options):
    defaults = vars(parse_args.parse([]))
    results = {}

    for k, v in defaults.items():
        opts = [o for o in list(options) if k.startswith(o)]
        values = [options.pop(o) for o in opts] or [v]
        if len(values) > 1:
            yield f'Ambiguous options {opts}'
        results[k] = values[-1]

    if options:
        yield f'Unknown options {options}'
        options.clear()

    options.update(results)
