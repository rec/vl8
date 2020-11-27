from vl8 import config
from vl8.config.config import merge
import unittest


class TestConfig(unittest.TestCase):
    def test_to_section(self):
        assert config.to_section('s') == 'sources'
        assert config.to_section('ta') == 'tasks'

        for bad in '', 'x', 'sa', 'taskso':
            with self.assertRaises(ValueError) as m:
                config.to_section(bad)
            assert (
                m.exception.args[0] == 'Do not understand section "%s"' % bad
            )

    def test_merge(self):
        assert merge([]) == {}

        c1 = {'so': {'foo': ['a', 'b']}, 'fu': {'bar': {'bing': 'bong'}}}

        assert merge([]) == {}
        expected = {
            'sources': {'foo': ['a', 'b']},
            'functions': {'bar': {'bing': 'bong'}},
        }
        assert merge([c1]) == expected

        c2 = {
            'sources': {'foo': ['c', 'd']},
            'functions': {'bar': {'bop': 'bop'}},
            'tasks': {},
        }
        assert merge([c2]) == c2

        expected = {
            'functions': {'bar': {'bop': 'bop'}},
            'tasks': {},
            'sources': {'foo': ['c', 'd']},
        }
        assert merge([c1, c2]) == expected

        expected = {
            'functions': {'bar': {'bing': 'bong', 'bop': 'bop'}},
            'tasks': {},
            'sources': {'foo': ['a', 'b', 'c', 'd']},
        }
        assert merge([c1, c2], overwrite=False) == expected
