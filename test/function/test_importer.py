from vl8.function import importer
import unittest


class TestImporter(unittest.TestCase):
    def test_importer(self):
        imp = importer('test.function.test_importer.TestImporter')
        assert imp is TestImporter

    def test_importer_guess(self):
        imp = importer('test.function.test_importer')
        assert imp is TestImporter
