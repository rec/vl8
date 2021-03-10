from unittest import mock
from vl8.function import separate_commands
import unittest


class TestIsFunction(unittest.TestCase):
    def test_is_function(self):
        for i in 'cut', 'tricky.wav()', 'first.second':
            assert separate_commands.is_function(i)

        for i in 'cut.wav', 'tricky.wav()', 'first.second':
            assert separate_commands.is_function(i)


@mock.patch('vl8.function.separate_commands.is_function', str.isupper)
class TestSeparateCommands(unittest.TestCase):
    def test_separate_commands(self):
        actual = list(separate_commands('aBcDEFg'))
        expected = [['B', ['a', 'c']], ['D', []], ['E', []], ['F', ['g']]]
        assert actual == expected

    def test_separate_commands2(self):
        actual = list(separate_commands('AbCdefG'))
        expected = [['A', ['b']], ['C', ['d', 'e', 'f']], ['G', []]]
        assert actual == expected

    def test_separate_commands3(self):
        actual = list(separate_commands('abcdefg'))
        expected = [[None, ['a', 'b', 'c', 'd', 'e', 'f', 'g']]]
        assert actual == expected

    def test_separate_commands4(self):
        actual = list(separate_commands('ABCDEFG'))
        expected = [
            ['A', []],
            ['B', []],
            ['C', []],
            ['D', []],
            ['E', []],
            ['F', []],
            ['G', []],
        ]
        assert actual == expected
