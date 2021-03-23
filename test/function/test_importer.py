from vl8.function import importer
from vl8.functions.catenate import Catenate
import unittest


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
        with self.assertRaises(ImportError) as m:
            importer('toast.function.test_importer')
        assert m.exception.args[0] == "No module named 'toast'"

    def test_import_error2(self):
        with self.assertRaises(ImportError) as m:
            importer('test.function.toast_importer')
        msg = 'No attribute in test.function named toast_importer'
        assert m.exception.args[0] == msg

    def test_import_error3(self):
        with self.assertRaises(ValueError) as m:
            importer('test.function.test_importer.unittest')

        assert m.exception.args[0].startswith(
            'Nothing callable in test.function.test_importer.unittest'
        )
