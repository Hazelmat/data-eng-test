.PHONY: help setup test clean release format install docker run

.DEFAULT_GOAL = help

TAG:=dev$(shell echo `date '+%Y%m%d%H%M%S'`)

help:
	@echo "---------------HELP-----------------"
	@echo "To setup the project type make setup"
	@echo "To test the project type make test"
	@echo "To run the project type make run"
	@echo "------------------------------------"

format:
	pre-commit run --all-files

install:
	pip install -r requirements-dev.txt
	pip install -r requirements.txt

docker:
	@echo -n "Building docker image with tag $(TAG)"
	docker build -f Dockerfile --platform linux/x86_64 -t eu.gcr.io/servier-data/mentions_pipeline:$(TAG) .

test:
	pytest tests

clean:
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf .mypy_cache/

run:
	pyflyte run src/workflow/drugs_workflow.py drugs_workflow --input_file src/resources/drugs.csv --prefix output
	pyflyte run src/workflow/clinical_trials_workflow.py clinical_trials_workflow --input_file src/resources/clinical_trials.csv --prefix output
	pyflyte run src/workflow/pubmed_workflow.py pubmed_workflow --input_file src/resources/pubmed.csv --prefix output
	pyflyte run src/workflow/pubmed_workflow.py pubmed_workflow --input_file src/resources/pubmed.json --prefix output
	pyflyte run src/workflow/drugs_mentions_workflow.py drugs_mentions_workflow --drugs_input_uri output/drugs --pubmed_input_uri  output/pubmed --clinical_trials_input_uri output/clinical_trials --prefix output