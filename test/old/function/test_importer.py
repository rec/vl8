from old.vl8.function import importer
from old.vl8.functions.catenate import Catenate
import unittest

MISSING = []


class TestImporter(unittest.TestCase):
    def test_trivial(self):
        imp = importer("test.old.function.test_importer.TestImporter")
        assert imp is TestImporter

    def test_function(self):
        assert importer("cat") is Catenate
        assert importer("c") is Catenate

    def test_guess(self):
        imp = importer("test.old.function.test_importer")
        assert imp is TestImporter

    def test_import_error1(self):
        mod = "toast.function.test_importer"
        with self.assertRaises(ImportError) as m:
            importer(mod)
        msg = (
            "toast.function.test_importer can't be found anywhere: "
            "('', 'old.vl8.functions.', 'old.vl8.functions.gen.')"
        )
        assert m.exception.args[0] == msg

    def test_import_error2(self):
        with self.assertRaises(ImportError) as m:
            importer("test.old.function.toast_importer")
        msg = (
            "test.old.function.toast_importer can't be found anywhere: "
            "('', 'old.vl8.functions.', 'old.vl8.functions.gen.')"
        )
        assert m.exception.args[0] == msg

    def test_import_error3(self):
        with self.assertRaises(ImportError) as m:
            importer("test.old.function.test_importer.unittest")

        assert m.exception.args == ("Nothing callable in unittest",)
