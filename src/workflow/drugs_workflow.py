from flytekit import task, workflow

from src.pipeline.drugs_job import run


@task
def drugs_task(input_file: str, prefix: str) -> str:
    output_uri = f"{prefix}/drugs/output"
    run(input_file, output_uri)
    return f"{prefix}/drugs"


@workflow
def drugs_workflow(input_file: str, prefix: str) -> str:
    return drugs_task(input_file=input_file, prefix=prefix)  # type: ignore
