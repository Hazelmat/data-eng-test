from flytekit import task, workflow

from src.pipeline.drugs_job import run


@task
def drugs_task(input_file: str, prefix: str):
    output_uri = f"{prefix}/drugs/output"
    run(input_file, output_uri)


@workflow
def drugs_workflow(input_file: str, prefix: str):
    drugs_task(input_file=input_file, prefix=prefix)
