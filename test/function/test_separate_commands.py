from vl8.function import separate_commands
import unittest


class TestConfig(unittest.TestCase):
    def test_is_function(self):
        for i in 'cut', 'tricky.wav()', 'first.second':
            assert separate_commands.is_function(i)

        for i in 'cut.wav', 'tricky.wav()', 'first.second':
            assert separate_commands.is_function(i)

    def test_separate_commands(self):
        actual = separate_commands('aBcDEFg', str.isupper)
        expected = [['B', ['a', 'c']], ['D', []], ['E', []], ['F', ['g']]]
        assert actual == expected

    def test_separate_commands2(self):
        actual = separate_commands('AbCdefG', str.isupper)
        expected = [['A', ['b']], ['C', ['d', 'e', 'f']], ['G', []]]
        assert actual == expected

    def test_separate_commands3(self):
        actual = separate_commands('abcdefg', str.isupper)
        expected = [[None, ['a', 'b', 'c', 'd', 'e', 'f', 'g']]]
        assert actual == expected

    def test_separate_commands4(self):
        actual = separate_commands('ABCDEFG', str.isupper)
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
