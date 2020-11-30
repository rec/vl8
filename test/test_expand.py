from vl8.config.expand import Expander
import unittest

expander = Expander('config', {'money': 3, 'love': 10})


class TestExpander(unittest.TestCase):
    def expand(self, **config):
        self.config = config
        self.errors = list(expander(self.config))

    def test_empty(self):
        self.expand()
        assert self.errors == []
        assert self.config == {'money': 3, 'love': 10}

    def test_simple(self):
        self.expand(m=5)
        assert self.errors == []
        assert self.config == {'money': 5, 'love': 10}

        self.expand(mo=5, love=20)
        assert self.errors == []
        assert self.config == {'money': 5, 'love': 20}

    def test_errors(self):
        self.expand(p=5)
        assert self.errors == ["Unknown config {'p': 5}"]

        self.expand(loves=5)
        assert self.errors == ["Unknown config {'loves': 5}"]
