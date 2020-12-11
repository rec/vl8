from pathlib import Path
from vl8.config import validate
import functools
import unittest


class TestValidate(unittest.TestCase):
    def validate(self, **kwargs):
        self.config = kwargs
        self.errors = list(validate.validate(self.config))

    def test_empty(self):
        self.validate()
        assert self.errors == []
        assert self.config == {
            'arguments': {
                'arguments': None,
                'continue': False,
                'dry_run': False,
                'verbose': False},
            'functions': {},
            'options': {'continue': False, 'dry_run': False, 'verbose': False},
            'sources': {},
            'tasks': {},
        }

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

        assert self.config == {
            'arguments': {
                'arguments': None,
                'continue': False,
                'dry_run': False,
                'verbose': False},
            'options': {'continue': False, 'dry_run': False, 'verbose': False},
            'sources': {'_': [Path('foo.wav')]},
            'tasks': {},
        }
