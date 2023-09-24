import apache_beam as beam

from src.metric.counter import CountingTransform
from src.metric.utils import get_counter


def process_pubmed(drug, records):
    """
    Process PubMed records and find mentions of the drug.

    :param dict drug: A dictionary representing the drug.
    :param list records: A list of dictionaries representing PubMed records.
    :return: A dictionary containing the ATC code of the drug and the mentions in PubMed.
    :rtype: tuple keyed by DrugId
    """
    mentions = []
    for record in records:
        if drug["drug"].lower() in record["title"].lower():
            mentions.append(
                {record["journal"].lower(): {"date": record["date"].isoformat(), "title": record["title"]}}
            )
    return (drug["atccode"], {"pubmed": mentions})


def process_clinical_trials(drug, records):
    """
    Process clinical trials records and find mentions of the drug.

    :param dict drug: A dictionary representing the drug.
    :param list records: A list of dictionaries representing clinical trials records.
    :return: A dictionary containing the ATC code of the drug and the mentions in clinical trials.
    :rtype: tuple keyed by DrugId
    """
    mentions = []
    for record in records:
        if drug["drug"].lower() in record["scientific_title"].lower():
            mentions.append(
                {record["journal"].lower(): {"date": record["date"].isoformat(), "title": record["scientific_title"]}}
            )
    return (drug["atccode"], {"clinical_trials": mentions})


def merge_dicts(data):
    """
    Merge PubMed and Clinical Trials dictionaries.

    :param tuple data: A tuple containing the key and values dictionaries.
    :return: A merged dictionary.
    :rtype: dict
    """
    key, values_dict = data
    pubmed_list = [item for sublist in values_dict["pubmed"] for item in sublist["pubmed"]]
    clinical_list = [item for sublist in values_dict["clinical_trials"] for item in sublist["clinical_trials"]]
    return {key: {"pubmed": pubmed_list, "clinical_trials": clinical_list}}


def run(
    drugs_input_uri: str,
    pubmed_input_uri: str,
    clinical_trials_input_uri: str,
    output_uri: str,
):
    """
    Run the Beam pipeline.

    :param str drugs_input_uri: URI of the input drugs data.
    :param str pubmed_input_uri: URI of the input PubMed data.
    :param str clinical_trials_input_uri: URI of the input Clinical Trials data.
    :param str output_uri: URI where the output json data will be written.
    """
    with beam.Pipeline() as p:
        drugs = (
            p
            | "Read Drugs" >> beam.io.ReadFromParquet(f"{drugs_input_uri}/*")
            | ("Count drugs input") >> CountingTransform("input_drugs_count")
        )

        pubmed = (
            p
            | "Read PubMed" >> beam.io.ReadFromParquet(f"{pubmed_input_uri}/*")
            | ("Count pubmed input") >> CountingTransform("input_pubmed_count")
        )
        clinical_trials = (
            p
            | "Read ClinicalTrials" >> beam.io.ReadFromParquet(f"{clinical_trials_input_uri}/*")
            | ("Count Clinical trials input") >> CountingTransform("input_clinical_trials_count")
        )

        # Find mentions in PubMed and Clinical Trials
        pubmed_pcol = drugs | "Map(mentioned_in_pubmed)" >> beam.Map(process_pubmed, beam.pvalue.AsIter(pubmed))
        clinical_pcol = drugs | "Map(mentioned_in_clinical_trials)" >> beam.Map(
            process_clinical_trials, beam.pvalue.AsIter(clinical_trials)
        )

        joined_collections = (
            {"clinical_trials": clinical_pcol, "pubmed": pubmed_pcol}
            | beam.CoGroupByKey()
            | "Merge Dictionaries" >> beam.Map(merge_dicts)
        )

        joined_collections | ("Count output") >> CountingTransform(
            "output_count"
        ) | "Write to JSON" >> beam.io.WriteToText(output_uri, file_name_suffix=".json")
    result = p.run()
    result.wait_until_finish()
    print(f"Input Drugs Count: {get_counter(result, 'input_drugs_count')} ")
    print(f"Input PubMed Count: {get_counter(result, 'input_pubmed_count')} ")
    print(f"Input ClinicalTrials Count: {get_counter(result, 'input_clinical_trials_count')} ")
    print(f"Output Count: {get_counter(result, 'output_count')} ")


if __name__ == "__main__":
    drugs_parquet = "output/drugs/output*.parquet"
    pubmed_parquet = "output/pubmed/output*.parquet"
    clinical_trials_parquet = "output/clinical_trials/output*.parquet"
    output_json = "output/drugs_mentions/output.json"
    run(drugs_parquet, pubmed_parquet, clinical_trials_parquet, output_json)
