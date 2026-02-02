from dataclasses import dataclass
from old.vl8.function.function import Function
import unittest


class TestFunction(unittest.TestCase):
    def test_simple_function1(self):
        f = Function("test.old.function.test_function.simp")
        assert f.type is f.Type.SIMPLE
        assert f("src", required=5) == ("src", 5, 1)

        with self.assertRaises(TypeError) as m:
            f("src")
        assert m.exception.args == (
            "simp() missing 1 required positional argument: 'required'",
        )

        with self.assertRaises(TypeError) as m:
            f("src", "src2", required=5)
        assert m.exception.args == (
            "test.old.function.test_function.simp takes exactly one argument",
        )

    def test_multi_function(self):
        f = Function("test.old.function.test_function.mult")
        assert f.type is f.Type.MULTIPLE
        assert f("src", required=5) == (("src",), 5, 1)
        assert f("s", "t", required=5) == (("s", "t"), 5, 1)

        with self.assertRaises(TypeError) as m:
            f("src")
        assert m.exception.args == (
            "mult() missing 1 required keyword-only argument: 'required'",
        )

    def test_simple_class(self):
        f = Function("test.old.function.test_function.Simp")
        assert f.type is f.Type.SIMPLE
        assert f("src", required=5) == ("src", 5, 1)

        with self.assertRaises(TypeError) as m:
            f("src")
        assert m.exception.args == (
            "__init__() missing 1 required positional argument: 'required'",
        )

        with self.assertRaises(TypeError) as m:
            f("src", "src2", required=5)
        assert m.exception.args == (
            "test.old.function.test_function.Simp takes exactly one argument",
        )

    def test_multi_class(self):
        f = Function("test.old.function.test_function.Mult")
        assert f.type is f.Type.MULTIPLE
        assert f("src", required=5) == (("src",), 5, 1)
        assert f("s", "t", required=5) == (("s", "t"), 5, 1)

        with self.assertRaises(TypeError) as m:
            f("src")
        assert m.exception.args == (
            "__init__() missing 1 required positional argument: 'required'",
        )


def simp(src, required, one=1):
    return src, required, one


def mult(*src, required, one=1):
    return src, required, one


@dataclass
class Simp:
    required: str
    one: int = 1

    def __call__(self, src):
        return src, self.required, self.one


@dataclass
class Mult:
    required: str
    one: int = 1

    def __call__(self, *src):
        return src, self.required, self.one
