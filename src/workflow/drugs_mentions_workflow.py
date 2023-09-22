from flytekit import task, workflow

from src.pipeline.drugs_mentions_graph_job import run


@task
def drugs_mentions_task(drugs_input_uri: str, pubmed_input_uri: str, clinical_trials_input_uri: str, prefix: str):
    output_uri = f"{prefix}/drugs_mentions/output"
    run(
        drugs_input_uri=drugs_input_uri,
        pubmed_input_uri=pubmed_input_uri,
        clinical_trials_input_uri=clinical_trials_input_uri,
        output_uri=output_uri,
    )


@workflow
def drugs_mentions_workflow(drugs_input_uri: str, pubmed_input_uri: str, clinical_trials_input_uri: str, prefix: str):
    drugs_mentions_task(
        drugs_input_uri=drugs_input_uri,
        pubmed_input_uri=pubmed_input_uri,
        clinical_trials_input_uri=clinical_trials_input_uri,
        prefix=prefix,
    )
