import unittest
from datetime import date

from src.pipeline.utils import convert_to_date, sanitize


class TestSanitizeFunction(unittest.TestCase):
    def test_sanitize(self):
        print(sanitize('décodé" extra'))
        self.assertEqual(sanitize('décodé" extra'), "decode extra")


class TestConvertToDateFunction(unittest.TestCase):
    def test_convert_to_date(self):
        self.assertEqual(convert_to_date("15 September 2022"), date(2022, 9, 15))
        self.assertEqual(convert_to_date("15/09/2022"), date(2022, 9, 15))
        self.assertEqual(convert_to_date("2022-09-15"), date(2022, 9, 15))
        self.assertIsNone(convert_to_date("Unrecognized Format"))


if __name__ == "__main__":
    unittest.main()
