.PHONY: test app venv clean clean-pyc clean-env clean-tests trained-model features predictions database

# To reproduce the trained model object, run `make trained-model`


all: load_data features trained-model evaluate-model database

data/survey.csv: src/load_data.py config/config.yml
	python src/load_data.py --savecsv data/survey.csv

load_data: data/survey.csv

data/survey_cleaned.csv: data/survey.csv src/generate_features.py config/config.yml
	python src/generate_features.py --config config/config.yml --loadcsv data/survey.csv --savecsv data/survey_cleaned.csv

features: data/survey_cleaned.csv

models/sample/random_forest.pkl: data/survey_cleaned.csv src/train_model.py config/config.yml
	python src/train_model.py --config config/config.yml --loadcsv data/survey_cleaned.csv --savemodel models/sample/random_forest.pkl

trained-model: models/sample/random_forest.pkl


evaluate-model: models/sample/random_forest.pkl data/X.csv data/y.csv config/config.yml src/evaluate_model.py
	python src/evaluate_model.py --config config/config.yml --loadmodel models/sample/random_forest.pkl

app: models/sample/random_forest.pkl app.py config/flask_config.py database
	python app.py


# Below are some other make functions that do useful things

# Create a virtual environment named pennylane-env
mentalhealth-env/bin/activate: requirements.txt
	test -d mentalhealth-env || virtualenv mentalhealth-env
	. mentalhealth-env/bin/activate; pip install -r requirements.txt
	touch mentalhealth-env/bin/activate

venv: mentalhealth-env/bin/activate

# Create the database
data/user_predictions.db:
	python src/database.py

database: data/user_predictions.db



# Run all tests
test:
	py.test

# Clean up things
clean-tests:
	rm -rf test/__pycache__

clean-src:
	rm -rf src/__pycache__

clean_data:
	rm -rf data/*.csv
	rm -rf data/*.db
	rm -rf models/sample/*.pkl

clean-env:
	rm -r mentalhealth-env

clean-pyc:
	find . -name '*pycache' -exec rm -f {} +
	rm -rf __pycache__

clean: clean-tests clean-src clean-pyc clean_data