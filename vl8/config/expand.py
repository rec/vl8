from dataclasses import dataclass


@dataclass
class Expander:
    name: str
    defaults: dict

    def __call__(self, config):
        results = {}

        for k, v in self.defaults.items():
            opts = [c for c in list(config) if k.startswith(c)]
            if len(opts) > 1:
                yield f'Ambiguous {self.name} {opts}'
            values = [config.pop(c) for c in opts]
            if values:
                v = values[-1]
            if callable(v):
                v = v()
            results[k] = v

        if config:
            yield f'Unknown {self.name} {config}'
            config.clear()

        config.update(results)
