from flytekit import task, workflow

from src.pipeline.clinical_trials_job import run


@task
def clinical_trials_task(input_file: str, prefix: str) -> str:  # type: ignore
    output_uri = f"{prefix}/clinical_trials/output"
    run(input_file, output_uri)
    return f"{prefix}/clinical_trials"


@workflow
def clinical_trials_workflow(input_file: str, prefix: str) -> str:  # type: ignore
    return clinical_trials_task(input_file=input_file, prefix=prefix)  # type: ignore
