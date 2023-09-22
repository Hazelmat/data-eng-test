import csv
import json
from io import StringIO

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from src.metric.counter import CountingTransform
from src.metric.utils import get_counter
from src.pipeline.schemas import pubmed_schema
from src.pipeline.utils import convert_to_date, sanitize


def transform_row(row):
    row["id"] = str(row["id"])
    row = {k: sanitize(v) for k, v in row.items()}
    row["date"] = convert_to_date(row["date"])
    return row


def filter_empty_id(record):
    return record["id"] != ""


def determine_file_type(filename):
    if filename.endswith(".json"):
        return "json"
    elif filename.endswith(".csv"):
        return "csv"
    else:
        raise ValueError(f"Unsupported file type for {filename}")


# Open the file and read its content


def read_input_file(p, filename):
    file_type = determine_file_type(filename)

    if file_type == "csv":
        return (
            p
            | "Read CSV" >> beam.io.ReadFromText(filename, skip_header_lines=1)
            | "Parse CSV" >> beam.ParDo(ParseCsvDoFn())
        )
    elif file_type == "json":
        with open(filename, "r") as file:
            file_content = file.read().strip().replace("\n", "").replace("},]", "}]")
            data = json.loads(file_content)
        return p | "Read JSON File" >> beam.Create(data)
    else:
        raise ValueError(f"Unsupported file type {file_type}")


class ParseCsvDoFn(beam.DoFn):
    def process(self, element):
        for row in csv.reader(StringIO(element)):
            if len(row) == 4:
                yield {"id": row[0], "title": row[1], "date": row[2], "journal": row[3]}


def run(input_file: str, output_uri: str):
    with beam.Pipeline(options=PipelineOptions()) as p:
        input_count = read_input_file(p, filename=input_file)

        transformed = (
            input_count
            | "Count Input" >> CountingTransform("input_count")
            | "Transform Rows" >> beam.Map(transform_row)
            | "Count Output" >> CountingTransform("output_count")
        )

        transformed | "Write to Parquet" >> beam.io.WriteToParquet(
            output_uri, schema=pubmed_schema, file_name_suffix=".parquet"
        )
    result = p.run()
    result.wait_until_finish()
    print(f"Input Count: {get_counter(result,'input_count')} ")
    print(f"Output Count: {get_counter(result,'output_count')} ")


if __name__ == "__main__":
    input_file = "pubmed.csv"
    output_parquet = "output/pubmed/pubmed.parquet"
    run(input_file, output_parquet)
