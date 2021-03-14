from vl8.function import FunctionCall
import unittest


class TestFunctionCall(unittest.TestCase):
    def test_a_simple_function(self):
        f = FunctionCall('test.function.test_function.simp(required: true)')
        assert f.func.is_simple
        assert f.missing == set()
        assert tuple(f('one')) == (('one', True, 1),)

    def test_simple_function2(self):
        f = FunctionCall('test.function.test_function.simp(r: true)')
        assert f.func.is_simple
        assert f.missing == set()
        assert tuple(f('one')) == (('one', True, 1),)

    def test_simple_error(self):
        f = FunctionCall('test.function.test_function.simp')
        assert f.func.is_simple
        assert f.missing == {'required'}
        with self.assertRaises(TypeError) as m:
            list(f(0))
        assert m.exception.args == ("Missing required arguments {'required'}",)
