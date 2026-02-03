import unittest

from old.vl8.config.expand import Expander

expander = Expander("config", {"money": 3, "love": 10, "murder": 0})


class TestExpander(unittest.TestCase):
    def expand(self, **config):
        self.config = config
        self.errors = list(expander(self.config))

    def test_empty(self):
        self.expand()
        assert self.errors == []
        assert self.config == {"money": 3, "love": 10, "murder": 0}

    def test_simple(self):
        self.expand(money=5)
        assert self.errors == []
        assert self.config == {"money": 5, "love": 10, "murder": 0}

        self.expand(mo=5, love=20)
        assert self.errors == []
        assert self.config == {"money": 5, "love": 20, "murder": 0}

    def test_errors(self):
        self.expand(m=5)
        assert self.errors == ["Ambiguous config m=5: ['money', 'murder']"]

        self.expand(p=5)
        assert self.errors == ["Unknown config: p=5"]

        self.expand(loves=5)
        assert self.errors == ["Unknown config: loves=5"]
