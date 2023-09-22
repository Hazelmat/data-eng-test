from flytekit import task, workflow

from src.pipeline.pubmed_job import run


@task
def pubmed_task(input_file: str, prefix: str):
    suffix = input_file.split(".")[1]
    output_uri = f"{prefix}/pubmed/output-{suffix}"
    run(input_file, output_uri)


@workflow
def pubmed_workflow(input_file: str, prefix: str):
    pubmed_task(input_file=input_file, prefix=prefix)
