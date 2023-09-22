import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from src.metric.counter import CountingTransform
from src.metric.utils import get_counter
from src.pipeline.schemas import drugs_schema
from src.pipeline.utils import sanitize


def transform_row(row):
    row = [sanitize(entry) for entry in row]
    return {"atccode": row[0], "drug": row[1]}


def run(input_csv: str, output_uri: str):
    with beam.Pipeline(options=PipelineOptions()) as p:
        input_count = (
            p
            | "Read CSV" >> beam.io.ReadFromText(input_csv, skip_header_lines=1)
            | "Count Input" >> CountingTransform("input_count")
            | "Split CSV" >> beam.Map(lambda line: line.split(","))
        )

        transformed = input_count | "Transform Rows" >> beam.Map(transform_row)

        (
            transformed
            | "Count Output" >> CountingTransform("output_count")
            | "Write to Parquet"
            >> beam.io.WriteToParquet(output_uri, schema=drugs_schema, file_name_suffix=".parquet")
        )
    result = p.run()
    result.wait_until_finish()
    print(f"Input Count: {get_counter(result,'input_count')} ")
    print(f"Output Count: {get_counter(result,'output_count')} ")


if __name__ == "__main__":
    input_csv = "drugs.csv"
    output_parquet = "output/drugs/drugs.parquet"
    run(input_csv, output_parquet)
