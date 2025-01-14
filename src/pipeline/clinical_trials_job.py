import csv
from io import StringIO

import apache_beam as beam

from src.metric.counter import CountingTransform
from src.metric.utils import get_counter
from src.pipeline.schemas import clinical_trials_schema
from src.pipeline.utils import convert_to_date, sanitize


class ParseCsvDoFn(beam.DoFn):
    """
    A DoFn class for parsing CSV lines into dictionaries.
    """

    def process(self, element):
        """
        Parse a CSV row into a dictionary.

        :param str element: A single row from the CSV file.
        :yield: A dictionary representing the parsed CSV row.
        :rtype: dict
        """
        for row in csv.reader(StringIO(element)):
            yield {
                "id": row[0],
                "scientific_title": row[1],
                "date": row[2],
                "journal": row[3],
            }


def transform_row(row):
    """
    Transform a row by sanitizing its values and converting date strings to date objects.

    :param dict row: A dictionary representing a row.
    :return: The transformed row.
    :rtype: dict
    """
    row = {k: sanitize(v) for k, v in row.items()}
    row["date"] = convert_to_date(row["date"])
    return row


def run(input_file: str, output_uri: str):
    """
    Run the Beam pipeline to process and transform the input CSV file
    and write the output to a Parquet file.

    :param str input_file: The path to the input CSV file.
    :param str output_uri: The URI where the output Parquet file will be written.
    """
    with beam.Pipeline() as p:
        input_count = (
            p
            | "Read CSV" >> beam.io.ReadFromText(input_file, skip_header_lines=1)
            | "Count Input" >> CountingTransform("input_count")
            | "Parse CSV" >> beam.ParDo(ParseCsvDoFn())
        )

        transformed = input_count | "Transform Rows" >> beam.Map(transform_row)

        (
            transformed
            | "Count Output" >> CountingTransform("output_count")
            | "Write to Parquet"
            >> beam.io.WriteToParquet(output_uri, schema=clinical_trials_schema, file_name_suffix=".parquet")
        )
    result = p.run()
    result.wait_until_finish()
    print(f"Input Count: {get_counter(result,'input_count')} ")
    print(f"Output Count: {get_counter(result,'output_count')} ")


if __name__ == "__main__":
    input_csv = "clinical_trials.csv"
    output_parquet = "output/clinical_trials/clinical_trials.parquet"
    run(input_csv, output_parquet)
