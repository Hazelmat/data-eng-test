pyflyte run src/workflow/drugs_workflow.py drugs_workflow --input_file src/resources/drugs.csv --prefix output
pyflyte run src/workflow/clinical_trials_workflow.py clinical_trials_workflow --input_file src/resources/clinical_trials.csv --prefix output
pyflyte run src/workflow/pubmed_workflow.py pubmed_workflow --input_file src/resources/pubmed.csv,src/resources/pubmed.json --prefix output
pyflyte run src/workflow/drugs_mentions_workflow.py drugs_mentions_workflow --drugs_input_uri output/drugs --pubmed_input_uri  output/pubmed --clinical_trials_input_uri output/clinical_trials --prefix output
pyflyte run src/workflow/drugs_mentions_workflow.py drugs_mentions_one_click_workflow --drugs_input src/resources/drugs.csv --pubmed_input  src/resources/pubmed.csv,src/resources/pubmed.json --clinical_trials_input src/resources/clinical_trials.csv --prefix output


