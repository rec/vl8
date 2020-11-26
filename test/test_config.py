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
