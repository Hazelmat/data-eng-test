import apache_beam as beam

from src.metric.counter import CountingTransform
from src.metric.utils import get_counter


def process_pubmed(drug, records):
    mentions = []
    for record in records:
        if drug["drug"].lower() in record["title"].lower():
            mentions.append({record["journal"].lower(): record["date"].isoformat()})
    return {drug["atccode"]: {"pubmed": mentions}}


def process_clinical_trials(drug, records):
    mentions = []
    for record in records:
        if drug["drug"].lower() in record["scientific_title"].lower():
            mentions.append({record["journal"].lower(): record["date"].isoformat()})
    return {drug["atccode"]: {"clinical_trials": mentions}}


def merge_dicts(data):
    key, values_dict = data
    pubmed_list = [item for sublist in values_dict["pubmed"] for item in sublist["pubmed"]]
    clinical_list = [item for sublist in values_dict["clinical_trials"] for item in sublist["clinical_trials"]]
    return {key: {"pubmed": pubmed_list, "clinical_trials": clinical_list}}


def format_pub_med(element):
    key, value = list(element.items())[0]
    return key, {"pubmed": value["pubmed"]}


def format_clinical(element):
    key, value = list(element.items())[0]
    return key, {"clinical_trials": value["clinical_trials"]}


def run(
    drugs_input_uri: str,
    pubmed_input_uri: str,
    clinical_trials_input_uri: str,
    output_uri: str,
):
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
            | "Read ClinicalTrials" >> beam.io.ReadFromParquet(f"" f"{clinical_trials_input_uri}/*")
            | ("Count Clinical trials input") >> CountingTransform("input_clinical_trials_count")
        )

        # Find mentions in PubMed and Clinical Trials
        pubmed_res = drugs | "Map(mentioned_in_pubmed)" >> beam.Map(process_pubmed, beam.pvalue.AsIter(pubmed))
        clinical_res = drugs | "Map(mentioned_in_clinical_trials)" >> beam.Map(
            process_clinical_trials, beam.pvalue.AsIter(clinical_trials)
        )

        pubmed_pcol = pubmed_res | "Format pubmed" >> beam.Map(format_pub_med)
        clinical_pcol = clinical_res | "Format clinical_pcol" >> beam.Map(format_clinical)
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
    print(f"Input Drugs Count: {get_counter(result,'input_drugs_count')} ")
    print(f"Input PubMed Count: {get_counter(result,'input_pubmed_count')} ")
    print(f"Input ClinicalTrials Count: {get_counter(result,'input_clinical_trials_count')} ")
    print(f"Output Count: {get_counter(result,'output_count')} ")


if __name__ == "__main__":
    drugs_parquet = "output/drugs/output*.parquet"
    pubmed_parquet = "output/pubmed/output*.parquet"
    clinical_trials_parquet = "output/clinical_trials/output*.parquet"
    output_json = "output/drugs_mentions/output.json"
    run(drugs_parquet, pubmed_parquet, clinical_trials_parquet, output_json)
