from vl8 import config
import unittest


class TestConfig(unittest.TestCase):
    def test_to_section(self):
        assert config.to_section('s') == 'source'
        assert config.to_section('jo') == 'job'

        for bad in '', 'x', 'sa', 'jobo':
            with self.assertRaises(ValueError) as m:
                config.to_section(bad)
            assert (
                m.exception.args[0] == 'Do not understand section "%s"' % bad
            )

    def test_merge(self):
        assert config.merge([]) == {}

        c1 = {'so': {'foo': ['a', 'b']}, 'fu': {'bar': {'bing': 'bong'}}}

        assert config.merge([]) == {}
        expected = {
            'source': {'foo': ['a', 'b']},
            'function': {'bar': {'bing': 'bong'}},
        }
        assert config.merge([c1]) == expected

        c2 = {
            'source': {'foo': ['c', 'd']},
            'function': {'bar': {'bop': 'bop'}},
            'job': {},
        }
        assert config.merge([c2]) == c2

        expected = {
            'function': {'bar': {'bop': 'bop'}},
            'job': {},
            'source': {'foo': ['c', 'd']},
        }
        assert config.merge([c1, c2]) == expected

        expected = {
            'function': {'bar': {'bing': 'bong', 'bop': 'bop'}},
            'job': {},
            'source': {'foo': ['a', 'b', 'c', 'd']},
        }
        assert config.merge([c1, c2], overwrite=False) == expected
