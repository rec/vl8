from vl8.function.bound_function import BoundFunction
import unittest


class TestBoundFunction(unittest.TestCase):
    def test_a_simple_function(self):
        f = BoundFunction('test.function.test_function.simp(required: true)')
        assert f.missing == set()
        assert tuple(f('one')) == (('one', True, 1),)

    def test_simple_function2(self):
        f = BoundFunction('test.function.test_function.simp(r: true)')
        assert f.missing == set()
        assert tuple(f('one')) == (('one', True, 1),)

    def test_simple_error(self):
        f = BoundFunction('test.function.test_function.simp')
        assert f.missing == {'required'}
        with self.assertRaises(TypeError) as m:
            list(f(0))
        assert m.exception.args == ("Missing required arguments {'required'}",)
