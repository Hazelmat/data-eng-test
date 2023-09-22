# Data Engineering with Python and Apache Beam

## Objective
The main objective of this project is to create a well-structured, clear, and clean codebase focusing on data manipulation jobs and adherence to Python best practices. The project highlights essential elements for code that can be used in a production environment, demonstrating knowledge in designing data jobs and integrating them with workflow orchestrators.

## 1. Data
The project works with the following four data files:
- `drugs.csv`: Contains drug names with an ID (`atccode`) and a name (`drug`).
- `pubmed.csv`: Contains titles of PubMed articles (`title`) associated with a journal (`journal`) and a date (`date`), along with an ID (`id`).
- `pubmed.json`: Has the same structure as `pubmed.csv` but in JSON format.
- `clinical_trials.csv`: Contains scientific publications with a title (`scientific_title`), an ID (`id`), a journal (`journal`), and a date (`date`).

## 2. Implementation
The project is structured to construct a data pipeline for processing the aforementioned data and generating the desired output. The codebase is organized to accommodate future integrations and reuse by other data pipelines. The focus is on modularization, adherence to professional practices, and ensuring smooth integration with DAG-based job orchestrators.

## 3. Data Pipeline
The implemented data pipeline produces a single JSON file representing a graph of connections between different drugs and their mentions in various publications and journals, along with the associated dates. Business rules consider a drug mentioned if it is cited in the title of a publication or issued by a journal.

## 4. Ad-hoc Processing
An additional feature allows extracting the name of the journal that mentions the most diverse drugs from the JSON produced by the data pipeline.

## 5. Repository
The project is hosted on a git repository. You can clone and review the codebase from the provided link.

## 6. Further Considerations
Feedback and considerations for handling large data volumes and potential modifications for such scenarios are welcome.

## SQL
The SQL part of the project involves querying transactional data and product nomenclature data. The tasks include calculating daily sales revenue and determining sales of furniture and decorative items for each client over a specific period.

## Running the Project
### Prerequisites
- Ensure you have Python installed.
- Apache Beam is used for constructing the data pipeline.

### Installation
```sh
git clone <repository-link>
cd <repository-name>
pip install -r requirements.txt