from pathlib import Path


def parse(sources):
    for k, v in list(sources.items()):
        if not isinstance(v, list):
            yield 'source %s was not a list' % k
        elif not all(isinstance(i, str) for i in v):
            yield 'source %s was not a list of strings' % k
        else:
            sources[k] = [Path(i).expanduser() for i in v]
            no = [p for p in v if not p.exists()]
            if no:
                yield from ('source file %s does not exist' % i for i in no)
