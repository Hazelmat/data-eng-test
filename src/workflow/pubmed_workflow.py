from flytekit import task, workflow

from src.pipeline.pubmed_job import run


@task
def pubmed_task(input_file: str, prefix: str) -> str:
    for file in input_file.split(","):
        suffix = file.split(".")[1]
        output_uri = f"{prefix}/pubmed/output-{suffix}"
        run(file, output_uri)
    return f"{prefix}/pubmed"


@workflow
def pubmed_workflow(input_file: str, prefix: str) -> str:
    return pubmed_task(input_file=input_file, prefix=prefix)  # type: ignore
