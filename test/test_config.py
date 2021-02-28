from vl8.config.config import merge
from vl8.config.parse_args import is_function, separate_arguments
import unittest


class TestConfig(unittest.TestCase):
    def test_merge(self):
        assert merge([]) == {}

        c1 = {
            'sources': {'foo': ['a', 'b']},
            'functions': {'bar': {'bing': 'bong'}},
        }

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

    def test_is_function(self):
        for i in 'cut', 'tricky.wav()', 'first.second':
            assert is_function(i)

        for i in 'cut.wav', 'tricky.wav()', 'first.second':
            assert is_function(i)

    def test_separate_arguments(self):
        actual = separate_arguments('aBcDEFg', str.isupper)
        expected = [('B', ['a', 'c']), ('D', []), ('E', []), ('F', ['g'])]
        assert actual == expected

    def test_separate_arguments2(self):
        actual = separate_arguments('AbCdefG', str.isupper)
        expected = [('A', ['b']), ('C', ['d', 'e', 'f']), ('G', [])]
        assert actual == expected

    def test_separate_arguments3(self):
        actual = separate_arguments('abcdefg', str.isupper)
        expected = [(None, ['a', 'b', 'c', 'd', 'e', 'f', 'g'])]
        assert actual == expected

    def test_separate_arguments4(self):
        actual = separate_arguments('ABCDEFG', str.isupper)
        expected = [
            ('A', []),
            ('B', []),
            ('C', []),
            ('D', []),
            ('E', []),
            ('F', []),
            ('G', []),
        ]
        assert actual == expected
