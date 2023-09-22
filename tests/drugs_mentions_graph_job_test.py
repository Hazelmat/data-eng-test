import datetime

import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

from src.pipeline import drugs_mentions_graph_job


def test_process_pubmed():
    with TestPipeline() as p:
        input_data = [
            {"drug": "Drug1", "atccode": "Code1"},
        ]

        records = [
            {
                "title": "This title has Drug1",
                "journal": "Journal1",
                "date": datetime.date(2023, 9, 21),
            },
        ]

        expected_output = [{"Code1": {"pubmed": [{"journal1": "2023-09-21"}]}}]

        input_collection = p | "Create Input" >> beam.Create(input_data)
        actual_output = input_collection | "Process PubMed" >> beam.Map(
            drugs_mentions_graph_job.process_pubmed, records
        )
        assert_that(actual_output, equal_to(expected_output), label="Check Process PubMed")


def test_process_clinical_trials():
    with TestPipeline() as p:
        input_data = [
            {"drug": "Drug1", "atccode": "Code1"},
        ]

        records = [
            {
                "scientific_title": "This title has Drug1",
                "journal": "Journal1",
                "date": datetime.date(2023, 9, 21),
            },
        ]

        expected_output = [{"Code1": {"clinical_trials": [{"journal1": "2023-09-21"}]}}]

        input_collection = p | "Create Input" >> beam.Create(input_data)
        actual_output = input_collection | "Process Clinical Trials" >> beam.Map(
            drugs_mentions_graph_job.process_clinical_trials, records
        )

        assert_that(
            actual_output,
            equal_to(expected_output),
            label="Check Process Clinical Trials",
        )


def test_merge_dicts():
    with TestPipeline() as p:
        input_data = [
            (
                "Code1",
                {
                    "pubmed": [{"pubmed": [{"journal1": "2023-09-21"}]}],
                    "clinical_trials": [{"clinical_trials": [{"journal2": "2023-09-21"}]}],
                },
            )
        ]

        expected_output = [
            {
                "Code1": {
                    "pubmed": [{"journal1": "2023-09-21"}],
                    "clinical_trials": [{"journal2": "2023-09-21"}],
                }
            }
        ]

        input_collection = p | "Create Input" >> beam.Create(input_data)
        actual_output = input_collection | "Merge Dictionaries" >> beam.Map(drugs_mentions_graph_job.merge_dicts)
        assert_that(actual_output, equal_to(expected_output), label="Check Merge Dictionaries")


if __name__ == "__main__":
    test_process_pubmed()
