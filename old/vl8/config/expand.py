from dataclasses import dataclass


@dataclass
class Expander:
    name: str
    defaults: dict

    def __call__(self, config):
        results = {}

        for k, v in config.items():
            opts = [d for d in self.defaults if d.startswith(k)]
            if opts:
                if len(opts) > 1:
                    yield f"Ambiguous {self.name} {k}={v}: {opts}"
                results[opts[0]] = v
            else:
                yield f"Unknown {self.name}: {k}={v}"

        for k, v in self.defaults.items():
            if k not in results:
                results[k] = v() if callable(v) else v

        config.clear()
        config.update(results)
