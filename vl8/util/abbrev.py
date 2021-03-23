import xmod


@xmod
def abbrev(dc, key):
    """Expand abbreviated prefixes in a dict if possible"""
    try:
        return dc[key]
    except KeyError:
        pass
    kv = [(k, v) for k, v in dc.items() if k.startswith(key)]
    if not kv:
        raise KeyError(key)
    if len(kv) > 1:
        keys = [k for k, v in kv]
        raise KeyError(key, f'was ambiguous: {keys}')
    return kv[0][1]
