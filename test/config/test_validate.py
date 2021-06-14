from pathlib import Path
from vl8.config.validate import validate
import functools
import unittest


class TestValidate(unittest.TestCase):
    def validate(self, **kwargs):
        self.config = kwargs
        self.errors = list(validate.validate(self.config))

    def test_empty(self):
        self.validate()
        assert self.errors == []
        assert self.config == dict(_CONFIG, functions={})

    def test_simple(self):
        # TODO: restore this
        # self.validate(sources='foo.wav', functions={'foo': 'vl8.foo'})
        self.validate(
            sources={'_': ['foo.wav']}, functions={'foo': 'vl8.util.error'}
        )

        assert self.errors == []

        functions = self.config.pop('functions')
        assert isinstance(functions.pop('foo'), functools.partial)
        assert not functions

        sources = {'_': [Path('foo.wav')]}
        assert self.config == dict(_CONFIG, sources=sources)


_CONFIG = {
    'arguments': {},
    'options': {
        'continue': False,
        'dry_run': False,
        'fade': 0.2,
        'force': False,
        'format': '.wav',
        'gain': None,
        'normalize': None,
        'numbers': 'float32',
        'output': '',
        'sample_rate': None,
        'type': 'int16',
        'verbose': False,
    },
    'sources': {},
    'tasks': {},
}
