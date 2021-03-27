from vl8.function import importer
from vl8.functions.catenate import Catenate
import unittest

MISSING = []


class TestImporter(unittest.TestCase):
    def test_trivial(self):
        imp = importer('test.function.test_importer.TestImporter')
        assert imp is TestImporter

    def test_function(self):
        assert importer('cat') is Catenate
        assert importer('c') is Catenate

    def test_guess(self):
        imp = importer('test.function.test_importer')
        assert imp is TestImporter

    def test_import_error1(self):
        mod = 'toast.function.test_importer'
        with self.assertRaises(ImportError) as m:
            importer(mod)
        assert m.exception.args[0] == f"No module named '{mod}'"

    def test_import_error2(self):
        with self.assertRaises(ImportError) as m:
            importer('test.function.toast_importer')
        msg = "No module named 'test.function.toast_importer'"
        assert m.exception.args[0] == msg

    def test_import_error3(self):
        with self.assertRaises(ImportError) as m:
            importer('test.function.test_importer.unittest')

        assert m.exception.args == (
            'Nothing callable in test.function.test_importer.unittest',
        )
