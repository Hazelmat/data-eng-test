from flytekit import task, workflow

from src.pipeline.drugs_mentions_graph_job import run
from src.workflow.clinical_trials_workflow import clinical_trials_workflow
from src.workflow.drugs_workflow import drugs_workflow
from src.workflow.pubmed_workflow import pubmed_workflow


@task
def drugs_mentions_task(
    drugs_input_uri: str,
    pubmed_input_uri: str,
    clinical_trials_input_uri: str,
    prefix: str,
):
    """
    Task to run the drugs mentions graph job with the given inputs.

    :param str drugs_input_uri: URI of the input drugs data.
    :param str pubmed_input_uri: URI of the input PubMed data.
    :param str clinical_trials_input_uri: URI of the input clinical trials data.
    :param str prefix: Prefix for the output URI.
    """
    output_uri = f"{prefix}/drugs_mentions/output"
    run(
        drugs_input_uri=drugs_input_uri,
        pubmed_input_uri=pubmed_input_uri,
        clinical_trials_input_uri=clinical_trials_input_uri,
        output_uri=output_uri,
    )


@workflow
def drugs_mentions_workflow(
    drugs_input_uri: str,
    pubmed_input_uri: str,
    clinical_trials_input_uri: str,
    prefix: str,
):
    """
    Workflow to execute the drugs mentions task.

    :param str drugs_input_uri: URI of the input drugs data.
    :param str pubmed_input_uri: URI of the input PubMed data.
    :param str clinical_trials_input_uri: URI of the input clinical trials data.
    :param str prefix: Prefix for the output URI.
    """
    drugs_mentions_task(
        drugs_input_uri=drugs_input_uri,
        pubmed_input_uri=pubmed_input_uri,
        clinical_trials_input_uri=clinical_trials_input_uri,
        prefix=prefix,
    )


@workflow
def drugs_mentions_one_click_workflow(
    drugs_input: str,
    pubmed_input: str,
    clinical_trials_input: str,
    prefix: str,
):
    """
    One-click workflow to execute clinical trials, PubMed, drugs workflows, and the drugs mentions workflow.

    :param str drugs_input: Path to transformed input drugs data.
    :param str pubmed_input: Path to transformed input PubMed data.
    :param str clinical_trials_input: Path to transformed input clinical trials data.
    :param str prefix: Prefix for the output URI.
    :return: None
    """
    clinical_trials_input_uri = clinical_trials_workflow(input_file=clinical_trials_input, prefix=prefix)
    pubmed_input_uri = pubmed_workflow(input_file=pubmed_input, prefix=prefix)
    drugs_input_uri = drugs_workflow(input_file=drugs_input, prefix=prefix)
    drugs_mentions_workflow(
        drugs_input_uri=drugs_input_uri,
        pubmed_input_uri=pubmed_input_uri,
        clinical_trials_input_uri=clinical_trials_input_uri,
        prefix=prefix,
    )
