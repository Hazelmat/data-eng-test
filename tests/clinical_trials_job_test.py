import datetime
import unittest
from io import StringIO

import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

from src.pipeline.clinical_trials_job import (ParseCsvDoFn, filter_empty_id,
                                              transform_row)


class TestParseCsvDoFn(unittest.TestCase):
    def test_process(self):
        test_input = StringIO('"1","Title","2022-09-21","Journal"')
        expected_output = [{"id": "1", "scientific_title": "Title", "date": "2022-09-21", "journal": "Journal"}]

        with TestPipeline() as p:
            actual_output = (
                p | "Create" >> beam.Create([test_input.getvalue()]) | "Parse CSV" >> beam.ParDo(ParseCsvDoFn())
            )
            assert_that(actual_output, equal_to(expected_output))


class TestTransformRow(unittest.TestCase):
    def test_transform_row(self):
        input_row = {"id": "1", "scientific_title": " Title émeraude", "date": "09/09/2021", "journal": " Journal "}
        expected_output = {
            "id": "1",
            "scientific_title": "Title emeraude",
            "date": datetime.date(2021, 9, 9),
            "journal": "Journal",
        }

        self.assertEqual(transform_row(input_row), expected_output)


class TestFilterEmptyId(unittest.TestCase):
    def test_filter_empty_id(self):
        self.assertTrue(filter_empty_id({"id": "1"}))
        self.assertFalse(filter_empty_id({"id": ""}))


if __name__ == "__main__":
    unittest.main()
